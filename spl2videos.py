from sl2video.convert_words_to_sigml import Word2Sigml
from spl2sl.spl2sl import Slp2Sl
from config import config


class Spl2Videos:
    def __init__(self, vncore_path, vocab_path, vocab_embedding_path, xml_path, google_project_id):
        self.slp2sl_obj = Slp2Sl(vncore_path, vocab_path, vocab_embedding_path, google_project_id)
        self.word2_sigml = Word2Sigml(xml_path)

    def convert(self, sent):
        sl_sent_info = self.slp2sl_obj.spl2sl(sent)
        sl_sent = self.word2_sigml.convert_words_to_sigml(sl_sent_info)
        return sl_sent


if __name__ == '__main__':

    spl2video_obj = Spl2Videos(config['vncore_path'], config['vocab_path'], config['vocab_embedding_path'], config['xml_path'], config['google_project_id'])
    sent = "Nhân dân rất quan tâm, muốn biết chủ trương, quan điểm của thành phố trong việc sáp nhập quận Hoàn Kiếm, bởi đây là quận trung tâm văn hóa, chính trị, kinh tế của Thủ đô, có bề dày truyền thống về văn hóa, lịch sử."
    sp_sent = spl2video_obj.convert(sent)
    with open(f'{config["output_path"]}/res.xml', 'w') as f:
        f.write(sp_sent)
