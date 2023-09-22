from spl2sl.shorten_sent import VertexAIModel
from spl2sl.translate import GoogleTranslate
from spl2sl.spl_sl_grammar_translate import GrammarTranslate
from spl2sl.get_sim_words import SynonymSent


class Slp2Sl:
    def __init__(self, vncore_path, vocab_path, vocab_embedding_path,  project_id='test-ai-vision-356213'):
        self.vertex_ai_model = VertexAIModel(project_id)
        self.google_translate_obj = GoogleTranslate(project_id)
        #self.grammar_translate_obj = GrammarTranslate()
        self.synonym_sent_obj = SynonymSent(vncore_path, vocab_path, vocab_embedding_path)

    def spl2sl(self, sent):
        en_sentence = self.google_translate_obj.translate_text(sent, "vi", "en")
        # print("Eng translate: ", en_sentence)
        shorten_sent = self.vertex_ai_model.simplify_sent(en_sentence)
        # print("Shorten: ", shorten_sent)
        vi_sent = self.google_translate_obj.translate_text(shorten_sent, "en", "vi")
        # print("Viet short: ", vi_sent)
        syn_sent = self.synonym_sent_obj.get_synonym_sent(vi_sent, 0.5)
        # print("Syn_sent: ", syn_sent)
        #sl_sent = self.grammar_translate_obj.translate_sent(syn_sent)
        # print("Gram_sent: ", sl_sent)
        sl_sent = self.synonym_sent_obj.get_synonym_sent(syn_sent, 0.5)
        # print("Recorrect: ", sl_sent)
        return sl_sent

    def post_process(self, sl_sent):
        return self.synonym_sent_obj.segment(sl_sent)


if __name__ == '__main__':
    sent = "Cảng Trần Đề sẽ giúp giảm chi phí hàng hoá xuất, nhập khẩu, phát triển công nghiệp, tạo đột phá cho kinh tế Đồng bằng sông Cửu Long, theo ông Nguyễn Văn Thể."
    vncore_path="/mnt/hdd/thuonglc/study/sign-language-prototype/assets/vncore"
    vocab_path="/mnt/hdd/thuonglc/study/sign-language-prototype/assets/qipedc_sl_viet_word_list_no_phrase_normalized.json"
    vocab_embedding_path="/mnt/hdd/thuonglc/study/sign-language-prototype/assets/word_embeddings.npy"
    slp2sl_obj = Slp2Sl(vncore_path, vocab_path, vocab_embedding_path)
    sl_sent = slp2sl_obj.spl2sl(sent)
    print(sl_sent)


