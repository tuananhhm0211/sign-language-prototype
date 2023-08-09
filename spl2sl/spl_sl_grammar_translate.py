from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class GrammarTranslate:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-base")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("Thuong/vsl_baseline_2")
        self.model.to('cuda')

    def translate_sent(self, sentence, max_length=128):
        text = sentence + " </s>"
        encoding = self.tokenizer(text, return_tensors="pt")
        input_ids, attention_masks = encoding["input_ids"].to("cuda"), encoding["attention_mask"].to("cuda")
        outputs = self.model.generate(
            input_ids=input_ids, attention_mask=attention_masks,
            max_length=max_length,
            early_stopping=True
        )
        line = self.tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
        return line


if __name__ == '__main__':
    model = GrammarTranslate()
