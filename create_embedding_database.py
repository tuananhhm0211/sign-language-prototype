import openai
import json
import os
import numpy as np
import time
from tqdm import tqdm


# Set up the OpenAI API client
openai.api_key = "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"


def get_embedding(text):
    params = {
        "model": "text-embedding-ada-002",
        "input": text,
    }

    # Call the API to get the embeddings
    response = openai.Embedding.create(**params)
    # Extract the embeddings from the response
    embeddings = response["data"][0]["embedding"]
    return embeddings


def read_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    words = content.split("\n")
    if words[-1] == "":
        words = words[:-1]
    return words


# Save numpy embeddings to a file
def write_np_embeddings_to_file(embeddings, dest_file_path):
    np_embeddings = np.array(embeddings)
    np.save(dest_file_path, np_embeddings)


if __name__ == '__main__':
    # Define the path to the file containing the words
    file_path = "sl_vocabs.txt"
    dest_file_path = "20230715_sl_embeddings.npy"
    words = read_file(file_path)
    embeddings = []
    for word in tqdm(words):
        embeddings.append(get_embedding(word))
        time.sleep(1.1)
    write_np_embeddings_to_file(embeddings, dest_file_path)
