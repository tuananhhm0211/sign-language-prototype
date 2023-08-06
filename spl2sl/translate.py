from google.cloud import aiplatform
from google.cloud import translate_v2 as translate


class GoogleTranslate:
    def __init__(self, project_id='test-ai-vision-356213'):
        aiplatform.init(project=project_id)
        self.translate_client = translate.Client()

    def translate_text(self, text: str, source: str = "vi", target: str = "en") -> dict:
        if isinstance(text, bytes):
            text = text.decode("utf-8")
        result = self.translate_client.translate(text, source_language=source, target_language=target)
        return result["translatedText"]


if __name__ == '__main__':
    vi_sent = "Ngân hàng cần nhiều trách nhiệm hơn trong các vụ chuyển nhầm tiền"
    google_translate_obj = GoogleTranslate()
    en_sent = google_translate_obj.translate_text(vi_sent)
    print(en_sent)
