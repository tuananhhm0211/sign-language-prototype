from spl2sl.shorten_sent import VertexAIModel
from spl2sl.translate import GoogleTranslate
from spl2sl.spl_sl_grammar_translate import GrammarTranslate
from spl2sl.get_sim_words import SynonymSent


class Slp2Sl:
    def __init__(self, vncore_path, vocab_path, vocab_embedding_path,  project_id='test-ai-vision-356213'):
        self.vertex_ai_model = VertexAIModel(project_id)
        self.google_translate_obj = GoogleTranslate(project_id)
        self.grammar_translate_obj = GrammarTranslate()
        self.synonym_sent_obj = SynonymSent(vncore_path, vocab_path, vocab_embedding_path)

    def spl2sl(self, sent):
        en_sentence = self.google_translate_obj.translate_text(sent, "vi", "en")
        shorten_sent = self.vertex_ai_model.shorten_sent(en_sentence)
        vi_sent = self.google_translate_obj.translate_text(shorten_sent, "en", "vi")
        syn_sent = self.synonym_sent_obj.get_synonym_sent(vi_sent, 0.5)
        sl_sent = self.grammar_translate_obj.translate_sent(syn_sent)
        return sl_sent

    def post_process(self, sl_sent):
        return self.synonym_sent_obj.segment(sl_sent)


if __name__ == '__main__':
    sent = "Ngân hàng cần nhiều trách nhiệm hơn trong các vụ chuyển nhầm tiền"
    slp2sl_obj = Slp2Sl(vncore_path="vncorenlp/VnCoreNLP-1.1.1.jar", vocab_path="spl2sl/vocab.txt", vocab_embedding_path="spl2sl/vocab_embedding.npy")
    sl_sent = slp2sl_obj.spl2sl(sent)
    print(sl_sent)
    print(slp2sl_obj.post_process(sl_sent))

