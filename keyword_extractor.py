import os
from openai import OpenAI
import re

class KeywordExtractor:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
    
    def extract_keywords(self, text, num_keywords=5):
        """
        Atlasa atslēgvārdus no teksta, izmantojot OpenAI
        """
        try:
            prompt = f"""
            No šā teksta atlasi {num_keywords} vissvarīgākos atslēgvārdus.
            Atgriezi tikai atslēgvārdus, atdalītus ar komatu.
            
            Teksts: {text[:2000]}  # Ierobežojam teksta garumu
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu esi atslēgvārdu ekstrakcijas speciālists."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.3
            )
            
            keywords_text = response.choices[0].message.content.strip()
            # Notīra un sadala atslēgvārdus
            keywords = [kw.strip() for kw in keywords_text.split(',')]
            return keywords[:num_keywords]
            
        except Exception as e:
            print(f"Kļūda atslēgvārdu ekstrakcijā: {e}")
            # Fallback: atgriež pirmos vārdus no teksta
            words = re.findall(r'\b\w+\b', text.lower())
            return list(set(words))[:num_keywords]
