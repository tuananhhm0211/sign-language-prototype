from google.cloud import aiplatform
from vertexai.preview.language_models import TextGenerationModel
from spl2sl.translate import GoogleTranslate
import json
import openai
import re
from time import sleep
import os
from dotenv import load_dotenv


load_dotenv()
# Set up the OpenAI API client
openai.api_key = os.environ.get("OPENAI_API_KEY")


class VertexAIModel:
    def __init__(self, project_id='test-ai-vision-356213', temperature: float = 0.2):
        aiplatform.init(project=project_id)
        self.model = TextGenerationModel.from_pretrained("text-bison@001")
        self.parameters = {
            "temperature": temperature,
            "max_output_tokens": 128,
            "top_p": .8,
            "top_k": 40,
        }
        self.google_translate_obj = GoogleTranslate()

    def _extract_sent(self, text):
        pattern = r"<sentence>(.*?)<\/sentence>"
        matches = re.findall(pattern, text)
        sents = []
        for match in matches:
            sents.append(match)
        return sents

    def simplify_syntax(self, sentence):
        prompt_template = f"""
                        You are an linguist expert.
                        Do exactly the following instructions to simplify the sentence: {sentence}.
                        if the sentence is short, simple, just return the sentence.
                        if the sentence is long or complex or compound sentence. transform it into 2 simple sentences with same meaning and only use the words that 5 year-old child can understand.
                    put each result sentence between <sentence></sentence> tags.
                    """

        response = self.model.predict(
            prompt_template,
            **self.parameters,
        )
        sents = self._extract_sent(response.text)
        return sents

    def _call_api(self, sent, task, fn_name):
        response = self._chatgpt_call(sent, task, fn_name)
        sleep(21)
        return response

    def _chatgpt_call(self, query, tasks, fn_name):
        # Step 1: send the conversation and available functions to GPT
        messages = [{"role": "user",
                     "content": f"Simplify the sentence: {query}"}]
        functions = [
            {
                "name": fn_name,
                "description": f"{tasks}",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "simple_sentence": {
                            "type": "string",
                            "description": "simple syntax sentence"
                        }
                    },
                }
            }
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=functions,
            function_call="auto",  # auto is default, but we'll be explicit
        )
        response_message = response["choices"][0]["message"]

        if response_message.get("function_call"):
            function_args = json.loads(response_message["function_call"]["arguments"])
            print(function_args)
            return function_args.get("simple_sentence")
        else:
            return None

    def delete_words(self, sent):
        response = self._call_api(sent, "only process the short sentences, the input sentence param need to remove stop words, unnessary words as much as possible before input the function", "process_condense_sentence")
        return response

    def simplify_lexical(self, sent):
        response = self._call_api(sent, "process only sentences that only have common words, the input sentence param need to use only common words that 4 years can understand", "process_sent_with_simple_words")
        return response

    def _simplify_sent(self, sentence):
        sim_lexical = self.simplify_lexical(sentence)
        if sim_lexical is None:
            sim_lexical = sentence
        deleted_sent = self.delete_words(sim_lexical)
        if deleted_sent is None:
            deleted_sent = sim_lexical
        return deleted_sent

    def simplify_sent(self, sentence):
        en_sentence = self.google_translate_obj.translate_text(sentence, "vi", "en")
        sents = self.simplify_syntax(en_sentence)
        sent = ". ".join(sents)
        vi_sent = self.google_translate_obj.translate_text(sent, "en", "vi")
        sim_sent = self._simplify_sent(vi_sent)
        return sim_sent


if __name__ == '__main__':
    sent = "Dung and Lan meanwhile had received especially high amounts of money as bribes, causing social distress and people to lose faith, so they deserved sentences more severe than what prosecutors recommended"
    goog_model = VertexAIModel()
    print(goog_model.simplify_sent(sent))
