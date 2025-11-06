import os
from dotenv import load_dotenv
from text_processor import TextProcessor
from quiz_generator import QuizGenerator
from keyword_extractor import KeywordExtractor

def main():
    load_dotenv()
    
    if not os.getenv("HUGGINGFACE_API_KEY"):
        print("Kļūda: HUGGINGFACE_API_KEY nav atrasta .env failā")
        return
    
    text_processor = TextProcessor()
    keyword_extractor = KeywordExtractor()
    quiz_generator = QuizGenerator()
    
    print("=== AI Teksta Apstrādes Rīks ===")
    
    input_file = input("Ievadi teksta faila nosaukumu (piem., text.txt): ").strip()
    
    if not os.path.exists(input_file):
        print(f"Kļūda: Fails '{input_file}' netika atrasts")
        return
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()
        
        print(f"\nIelasīts teksts ({len(text)} rakstzīmes)")
        
        print("\n=== TEKSTA APKOPOŠANA ===")
        summary = text_processor.summarize_text(text)
        print(f"Apkopojums: {summary}")
        
        print("\n=== ATSLĒGVĀRDU ATLASĪŠANA ===")
        try:
            keyword_count = int(input("Ievadi vēlamo atslēgvārdu skaitu: "))
            keywords = keyword_extractor.extract_keywords(text, keyword_count)
            print(f"Atslēgvārdi: {', '.join(keywords)}")
        except ValueError:
            print("Kļūda: Ievadi derīgu skaitli")
        
        print("\n=== VIKTORĪNAS JAUTĀJUMU ĢENERĒŠANA ===")
        quiz_questions = quiz_generator.generate_quiz(text, num_questions=3)
        
        for i, question in enumerate(quiz_questions, 1):
            print(f"\n{i}. {question['question']}")
            for j, option in enumerate(question['options'], 1):
                print(f"   {chr(64+j)}) {option}")
            print(f"   Pareizā atbilde: {question['correct_answer']}")
            
    except Exception as e:
        print(f"Kļūda: {e}")

if __name__ == "__main__":
    main()
