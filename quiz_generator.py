import os
import re

class QuizGenerator:
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
    
    def generate_quiz(self, text, num_questions=3):
        """
        Ģenerē testa jautājumus - uzlabota versija
        """
        try:
            return self._generate_improved_quiz(text, num_questions)
        except Exception as e:
            print(f"Kļūda viktorīnas ģenerēšanā: {e}")
            return self._create_fallback_questions(num_questions)
    
    def _generate_improved_quiz(self, text, num_questions):
        """Uzlabota viktorīnas ģenerēšana no teksta"""
        questions = []
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 15]
        
        for i in range(min(num_questions, len(sentences))):
            if i < len(sentences):
                sentence = sentences[i]
                if len(sentence) > 20:
                    # Dažādi jautājumu veidi
                    question_types = [
                        f"Ko apraksta šis teikums: '{sentence[:80]}...'?",
                        f"Kāda ir galvenā doma: '{sentence[:80]}...'?",
                        f"Kas ir minēts teikumā: '{sentence[:80]}...'?"
                    ]
                    
                    question_text = question_types[i % len(question_types)]
                    
                    questions.append({
                        'question': question_text,
                        'options': [
                            "Pareizā atbilde (balstīts uz tekstu)",
                            "Nepareizs variants 1", 
                            "Nepareizs variants 2",
                            "Nepareizs variants 3"
                        ],
                        'correct_answer': "A"
                    })
        
        if not questions:
            return self._create_fallback_questions(num_questions)
        
        return questions
    
    def _create_fallback_questions(self, num_questions):
        """Fallback jautājumi par AI"""
        base_questions = [
            {
                'question': "Ko apzīmē saīsinājums MI?",
                'options': [
                    "Mākslīgais intelekts",
                    "Mašīnu izglītība", 
                    "Matemātiskā informātika",
                    "Mobilā ierīce"
                ],
                'correct_answer': "A"
            },
            {
                'question': "Kas ir mašīnmācīšanās?",
                'options': [
                    "MI apakšnozare, kas koncentrējas uz algoritmiem",
                    "Datoru montāžas process",
                    "Programmēšanas valoda",
                    "Datu bāzu veids"
                ],
                'correct_answer': "A"
            },
            {
                'question': "Kādi ir galvenie MI veidi?",
                'options': [
                    "Vājais MI un stiprais MI",
                    "Digitālais un analogais MI", 
                    "Vienkāršais un sarežģītais MI",
                    "Mājās un rūpnieciskais MI"
                ],
                'correct_answer': "A"
            }
        ]
        return base_questions[:num_questions]
