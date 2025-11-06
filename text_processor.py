import os
from huggingface_hub import InferenceClient

class TextProcessor:
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.client = InferenceClient(token=self.api_key)
    
    def summarize_text(self, text, max_length=150):
        """
        Apkopo tekstu, izmantojot summarization modeli
        """
        try:
            summary = self.client.summarization(
                text,
                model="facebook/bart-large-cnn"
            )
            return summary.summary_text
        except Exception as e:
            print(f"Kļūda teksta apkopošanā: {e}")
            sentences = text.split('.')
            if len(sentences) > 2:
                return '. '.join(sentences[:2]) + '.'
            return text[:147] + "..." if len(text) > 150 else text
