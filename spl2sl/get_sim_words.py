import numpy as np
import py_vncorenlp
import json
# import os
import fasttext
from huggingface_hub import hf_hub_download
from sklearn.metrics.pairwise import cosine_similarity


class SynonymSent:
    def __init__(self, vncore_path, vocab_path, vocab_embedding_path):
        py_vncorenlp.download_model(save_dir=vncore_path)
        self.seg_model = py_vncorenlp.VnCoreNLP(save_dir=vncore_path,  annotators=["wseg", "pos", "ner"])
        model_path = hf_hub_download(repo_id="facebook/fasttext-vi-vectors", filename="model.bin")
        self.word_model = fasttext.load_model(model_path)
        self.vocab_words = self._read_json(vocab_path)
        self.vocab_embeddings = np.load(vocab_embedding_path)
        self.finger_pos_list = ['Np', 'Ny', 'Ni', 'Np', 'NNP', 'Ny', 'M', 'E', 'Fw', 'FW', 'CH']
        self.remove_pos_list = ['I', 'L', 'T', 'X']

    def _read_json(self, vocab_path):
        with open(vocab_path, 'r', encoding="utf-8") as f:
            content = json.load(f)
        return content

    def segment(self, sentence):
        out = self.seg_model.annotate_text(sentence)
        return out[0]

    def get_k_candidate(self, query_vec, k=1):
        cos_sim = cosine_similarity(query_vec.reshape(1, -1), self.vocab_embeddings)
        most_similar_indices = np.argsort(cos_sim[0])[::-1]

        # Print the most similar words and their cosine similarities
        candidate_list = []
        for i in most_similar_indices[:k]:
            candidate_list.append([self.vocab_words[i], cos_sim[0][i]])
        return candidate_list

    def _get_most_sim_word(self, word):
        word = replace_all(word)
        vector = self.word_model.get_word_vector(word)
        candidate_list = self.get_k_candidate(vector, k=1)
        return candidate_list[0]

    def get_synonym_sent(self, sent, threshold=0.65):
        token_info_list = self.segment(sent)
        synonym_sent_list = []
        for token_info in token_info_list:
            if token_info['posTag'] in self.finger_pos_list:
                synonym_sent_list.append([token_info['wordForm'], token_info['posTag']])
            elif token_info['posTag'] in self.remove_pos_list:
                pass
            else:
                candidate = self._get_most_sim_word(token_info['wordForm'])
                if candidate[1] >= threshold:
                    synonym_sent_list.append([candidate[0], token_info['posTag']])
        syn_sent = ' '.join([i[0] for i in synonym_sent_list])
        syn_sent = syn_sent.replace("_", " ")
        return syn_sent


def replace_all(text):
    dict_map = {
            "òa": "oà",
            "Òa": "Oà",
            "ÒA": "OÀ",
            "óa": "oá",
            "Óa": "Oá",
            "ÓA": "OÁ",
            "ỏa": "oả",
            "Ỏa": "Oả",
            "ỎA": "OẢ",
            "õa": "oã",
            "Õa": "Oã",
            "ÕA": "OÃ",
            "ọa": "oạ",
            "Ọa": "Oạ",
            "ỌA": "OẠ",
            "òe": "oè",
            "Òe": "Oè",
            "ÒE": "OÈ",
            "óe": "oé",
            "Óe": "Oé",
            "ÓE": "OÉ",
            "ỏe": "oẻ",
            "Ỏe": "Oẻ",
            "ỎE": "OẺ",
            "õe": "oẽ",
            "Õe": "Oẽ",
            "ÕE": "OẼ",
            "ọe": "oẹ",
            "Ọe": "Oẹ",
            "ỌE": "OẸ",
            "ùy": "uỳ",
            "Ùy": "Uỳ",
            "ÙY": "UỲ",
            "úy": "uý",
            "Úy": "Uý",
            "ÚY": "UÝ",
            "ủy": "uỷ",
            "Ủy": "Uỷ",
            "ỦY": "UỶ",
            "ũy": "uỹ",
            "Ũy": "Uỹ",
            "ŨY": "UỸ",
            "ụy": "uỵ",
            "Ụy": "Uỵ",
            "ỤY": "UỴ",
        }
    for i, j in dict_map.items():
        text = text.replace(i, j)
    return text


if __name__ == '__main__':
    vncore_path = "/mnt/hdd/thuonglc/study/sign-language-prototype/assets/vncore"
    vocab_path = "/mnt/hdd/thuonglc/study/sign-language-prototype/assets/qipedc_sl_viet_word_list_no_phrase_normalized.json"
    vocab_embedding_path = "/mnt/hdd/thuonglc/study/sign-language-prototype/assets/word_embeddings.npy"
    vi_sentence = 'Nhiều tuyến đường vùng núi phía Bắc sạt lở vì mưa lũ'
    synonym_sent_ob = SynonymSent(vncore_path, vocab_path, vocab_embedding_path)
    synonym_sent = synonym_sent_ob.get_synonym_sent(vi_sentence, 0.5)
    print(synonym_sent)

