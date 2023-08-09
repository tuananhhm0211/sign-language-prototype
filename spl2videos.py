from sl2video.convert_words_to_sigml import Word2Sigml
from spl2sl.spl2sl import Slp2Sl


class Spl2Videos:
    def __init__(self, vncore_path, vocab_path, vocab_embedding_path, xml_path):
        self.slp2sl_obj = Slp2Sl(vncore_path, vocab_path, vocab_embedding_path)
        self.word2_sigml = Word2Sigml(xml_path)

    def convert(self, sent):
        sl_sent_info = self.slp2sl_obj.spl2sl(sent)
        sl_sent = self.word2_sigml.convert_words_to_sigml(sl_sent_info)
        return sl_sent


if __name__ == '__main__':
    xml_path = "/mnt/hdd/thuonglc/study/sign-language-prototype/assets/hamnosys2sigml"
    sent = "Nhân dân rất quan tâm, muốn biết chủ trương, quan điểm của thành phố trong việc sáp nhập quận Hoàn Kiếm, bởi đây là quận trung tâm văn hóa, chính trị, kinh tế của Thủ đô, có bề dày truyền thống về văn hóa, lịch sử."
    vncore_path="/mnt/hdd/thuonglc/study/sign-language-prototype/assets/vncore"
    vocab_path="/mnt/hdd/thuonglc/study/sign-language-prototype/assets/qipedc_sl_viet_word_list_no_phrase_normalized.json"
    vocab_embedding_path="/mnt/hdd/thuonglc/study/sign-language-prototype/assets/word_embeddings.npy"
    spl2video_obj = Spl2Videos(vncore_path, vocab_path, vocab_embedding_path, xml_path)
    sp_sent = spl2video_obj.convert(sent)
    with open('/mnt/hdd/thuonglc/study/sign-language-prototype/outputs/res.xml', 'w') as f:
        f.write(sp_sent)
