from vertexai.preview.language_models import TextGenerationModel
from google.cloud import aiplatform


class VertexAIModel:
    def __init__(self, project_id='test-ai-vision-356213', temperature: float = 0.2):
        aiplatform.init(project=project_id)
        self.model = TextGenerationModel.from_pretrained("text-bison@001")
        self.parameters = {
            "temperature": temperature,
            "max_output_tokens": 256,
            "top_p": .8,
            "top_k": 40,
        }

    def shorten_sent(self, sentence):
        response = self.model.predict(
            f'"{sentence}", make the sentence as short and simple as possible using simple words',
            **self.parameters,
        )
        return response.text


if __name__ == '__main__':
    sent = "Dung and Lan meanwhile had received especially high amounts of money as bribes, causing social distress and people to lose faith, so they deserved sentences more severe than what prosecutors recommended"
    goog_model = VertexAIModel()
    print(goog_model.shorten_sent(sent))
