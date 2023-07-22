import faiss
import numpy as np
import openai
from underthesea import word_tokenize
import json
from tqdm import tqdm
from time import sleep
import random
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def load_saved_embedding(file_path):
    embeddings = np.load(file_path)
    return embeddings


def read_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    words = content.split("\n")
    if words[-1] == "":
        words = words[:-1]
    return words


def get_k_neighbours(embeddings, query_embedding, k):
    # Create an index with the same dimensionality as your embeddings
    d = embeddings.shape[1]  # dimensionality
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    distances, indices = index.search(np.array([query_embedding]), k)
    return distances, indices


def get_embedding(text):
    params = {
        "model": "text-embedding-ada-002",
        "input": text,
    }

    # Call the API to get the embeddings
    response = openai.Embedding.create(**params)
    embeddings = response["data"][0]["embedding"]
    return embeddings


def get_k_words(words, indices):
    k_words = []
    for index in indices[0]:
        k_words.append(words[index])
    return k_words


def get_candidate_words(query, words, embeddings, k=20):
    query_word_list = word_tokenize(query)
    sub_vocab = []

    for query_word in tqdm(query_word_list):
        query_word.replace(" ", "_")
        query_embedding = get_embedding(query_word)
        sleep(20)
        distances, indices = get_k_neighbours(embeddings, query_embedding, k)
        k_words = get_k_words(words, indices)
        sub_vocab.extend(k_words)
    return sub_vocab


def get_similar_sentences_using_set_of_words(candidate_words, query_sent):
    candidate_words = [candidate_word.replace("_", " ") for candidate_word in candidate_words]
    print(candidate_words)
    candidate_str = ", ".join(candidate_words)

    translated_sent = translate_language(query_sent, language="french")
    sleep(20)
    sim_res = sl_translate(candidate_str, translated_sent)
    return sim_res


def sl_translate(word_vocab_str, query):
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": f"The vocab of my child is very limited, The vocab of my child including the following words: {word_vocab_str}. Translate the sentence into Vietnamese: '{query}"}]
    functions = [
        {
            "name": "translate_sentence_only_using_from_limited_words",
            "description": f"translate the sentence requiring only to use limited number of words user provided",
            "parameters": {
                "type": "object",
                "properties": {
                    "translated_sentence": {
                        "type": "string",
                        "description": "The translated sentence that only use only words user provided."
                    }
                },
            }
        }
    ]
    print("call function")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        function_args = json.loads(response_message["function_call"]["arguments"])
        print(function_args)
        return function_args.get("translated_sentence")
    else:
        return None


def translate_language(query, language="french"):
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": f"Translate the sentence '{query}' into {language}"},]
    functions = [
        {
            "name": "translate_sentence_into_french",
            "description": f"Translate the Vietnamese sentence into {language}",
            "parameters": {
                "type": "object",
                "properties": {
                    "translated_sentence": {
                        "type": "string",
                        "description": f"{language} sentence"
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

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        function_args = json.loads(response_message["function_call"]["arguments"])
        return function_args.get("translated_sentence")
    else:
        return None


if __name__ == '__main__':
    # Define the path to the file containing the words
    vocab_file_path = "./assets/filter_sl_vocab.txt"
    embedding_file_path = "./assets/sl_after_embeddings.npy"
    query = "Hôm nay rất vui vì được gặp mọi người"
    query = query.lower()
    words = read_file(vocab_file_path)
    embeddings = load_saved_embedding(embedding_file_path)
    candidate_word_list = get_candidate_words(query, words, embeddings)
    print(candidate_word_list)
    res = get_similar_sentences_using_set_of_words(candidate_word_list, query)
    print(query, "---->", res)
