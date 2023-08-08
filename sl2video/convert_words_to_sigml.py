from pathlib import Path
import xml.etree.ElementTree as ET
import os
from pprint import pprint


class Word2Sigml:
    def __init__(self, xml_dir):
        self.xml_dir = xml_dir
        self.words = [xml_path.stem for xml_path in list(Path(xml_dir).glob("*.xml"))]
        # print(len(self.words))

    def _read_file(self, file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        content = "\n".join(content.split("\n")[1:-1])
        return content


    def _combine_sigml_files(self, xml_name_list):
        xml_content = []
        for xml_name in xml_name_list:
            dest_path =  os.path.join(self.xml_dir, f"{xml_name}.xml")
            content = self._read_file(dest_path)[8:-8].strip()
            xml_content.append(content)

        xml_content_str = "\n".join(xml_content).strip()
        xml_str = f"""
                <sigml>
                {xml_content_str}
                </sigml>
                """
        # pprint(xml_str)
        return xml_str

    def convert_words_to_sigml(self, sent):
        xml_name_list = []
        for word in sent:
            if word in self.words:
                xml_name_list.append(word)
            else:
                xml_name_list.append(self.words[0])
        xml_str = self._combine_sigml_files(xml_name_list)  
        return xml_str
    
if __name__ == '__main__':
    word2_sigml = Word2Sigml("/mnt/hdd/thuonglc/study/sign-language-prototype/assets/hamnosys2sigml")
    sent = ['H', 'proof','phòng_y_tế', 'phòng_thư_viện']
    res = word2_sigml.convert_words_to_sigml(sent)
    with open('test.xml', 'w') as f:
        f.write(res)
