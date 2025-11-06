import os
from huggingface_hub import InferenceClient
import requests

class TextProcessor:
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.client = InferenceClient(token=self.api_key)
    
    def summarize_text(self, text, max_length=150):
        """
        Apkopo tekstu, izmantojot Hugging Face modeli
        """
        try:
            # Izmanto summarization modeli
            summary = self.client.summarization(
                text,
                parameters={"max_length": max_length}
            )
            return summary.summary_text
        except Exception as e:
            print(f"Kļūda teksta apkopošanā: {e}")
            # Fallback: atgriež pirmos 150 rakstzīmes
            return text[:147] + "..." if len(text) > 150 else text
