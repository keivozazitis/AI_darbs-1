import os
import json
from openai import OpenAI

class QuizGenerator:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
    
    def generate_quiz(self, text, num_questions=3):
        """
        Ģenerē testa jautājumus ar 4 atbilžu variantiem
        """
        try:
            prompt = f"""
            Uzraksti {num_questions} testa jautājumus pamatojoties uz šo tekstu.
            Katram jautājumam pievieno 4 iespējamās atbildes (tikai viena ir pareiza).
            Atgriezi atbildi JSON formātā:
            
            {{
                "questions": [
                    {{
                        "question": "jautājuma teksts",
                        "options": ["1. variants", "2. variants", "3. variants", "4. variants"],
                        "correct_answer": "A"
                    }}
                ]
            }}
            
            Teksts: {text[:3000]}  # Ierobežojam teksta garumu
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu esi viktorīnu jautājumu ģenerators. Atgriež tikai JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Mēģina parsēt JSON
            try:
                quiz_data = json.loads(result_text)
                return quiz_data.get("questions", [])
            except json.JSONDecodeError:
                print("Kļūda: Nevarēja parsēt JSON atbildi")
                return self._create_fallback_questions(text, num_questions)
                
        except Exception as e:
            print(f"Kļūda viktorīnas ģenerēšanā: {e}")
            return self._create_fallback_questions(text, num_questions)
    
    def _create_fallback_questions(self, text, num_questions):
        """Fallback jautājumi, ja API neizdodas"""
        questions = []
        for i in range(num_questions):
            questions.append({
                "question": f"Pamata jautājums {i+1} par tekstu",
                "options": ["1. variants", "2. variants", "3. variants", "4. variants"],
                "correct_answer": "A"
            })
        return questions
