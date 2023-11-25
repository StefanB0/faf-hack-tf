from transformers import pipeline
from googletrans import Translator


class SummaryGenerator:
    def __init__(self, model_path):
        self.sumarizer = pipeline("summarization", model=model_path)
        self.translator = Translator()

    def sumarize(self, text, max_length = 250, min_length = 100):
        text = " ".join(text.split())
        english_translation = self.translator.translate(text, dest="en")
        english_summary = self.sumarizer(english_translation.text, max_length=max_length, min_length=min_length, do_sample=False)
        romanian_translation = self.translator.translate(english_summary[0]["summary_text"], dest="ro")
        return romanian_translation.text