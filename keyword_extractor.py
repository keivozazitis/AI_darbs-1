import os
import re

class KeywordExtractor:
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
    
    def extract_keywords(self, text, num_keywords=5):
        """
        Atlasa atslēgvārdus no teksta
        """
        try:
            return self._extract_smart_keywords(text, num_keywords)
        except Exception as e:
            print(f"Kļūda atslēgvārdu ekstrakcijā: {e}")
            return self._extract_fallback_keywords(text, num_keywords)
    
    def _extract_smart_keywords(self, text, num_keywords):
        """Viedāka atslēgvārdu ekstrakcija"""
        # Noņem pieturzīmes un sadala teikumos
        sentences = re.split(r'[.!?]', text)
        
        keywords = []
        important_terms = [
            'mākslīgais intelekts', 'MI', 'mašīnmācīšanās', 'datu tehnoloģijas',
            'algoritmi', 'neuronu tīkli', 'datoru sistēmas', 'intelektuāla darbība',
            'runas atpazīšana', 'vizuala uztvere', 'valodu tulkošana', 'lēmumu pieņemšana'
        ]
        
        # Pievieno svarīgus terminus, kas atrodami tekstā
        for term in important_terms:
            if term.lower() in text.lower():
                keywords.append(term)
        
        # Ekstrakcija no teikumiem
        for sentence in sentences:
            words = re.findall(r'\b\w+\b', sentence.lower())
            # Atlasa garākus vārdus kā potenciālus atslēgvārdus
            long_words = [word for word in words if len(word) > 5]
            keywords.extend(long_words)
        
        # Noņem dublikātus un atgriež vajadzīgo skaitu
        unique_keywords = list(set(keywords))
        return unique_keywords[:num_keywords]
    
    def _extract_fallback_keywords(self, text, num_keywords):
        """Fallback atslēgvārdu ekstrakcija"""
        words = re.findall(r'\b\w+\b', text.lower())
        # Noņem īsos vārdus un izvēlas biežākos
        meaningful_words = [word for word in words if len(word) > 3]
        # Atgriež unikālos vārdus
        return list(set(meaningful_words))[:num_keywords]
