import faiss
import numpy as np
import openai
from underthesea import word_tokenize
import json
from tqdm import tqdm


# Set up the OpenAI API client
openai.api_key = "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"


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


def get_candidate_words(query, words, embeddings, k=30):
    query_word_list = word_tokenize(query)
    sub_vocab = []

    for query_word in tqdm(query_word_list):
        query_embedding = get_embedding(query_word)
        distances, indices = get_k_neighbours(embeddings, query_embedding, k)
        k_words = get_k_words(words, indices)
        sub_vocab.extend(k_words)
    return sub_vocab


if __name__ == '__main__':
    # Define the path to the file containing the words
    vocab_file_path = "/home/love_you/Documents/joyness/sign-language-prototype/assets/filter_sl_vocab.txt"
    embedding_file_path = "/home/love_you/Documents/joyness/sign-language-prototype/assets/sl_after_embeddings.npy"
    query = "cô ta đang chơi thể thao"
    query = query.lower()
    words = read_file(vocab_file_path)
    embeddings = load_saved_embedding(embedding_file_path)
    candidate_word_list = get_candidate_words(query, words, embeddings)
    print(candidate_word_list)



