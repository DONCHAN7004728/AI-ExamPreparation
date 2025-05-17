import sys
import mysql.connector
import google.generativeai as genai
import os
import codecs

os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("HTTP_PROXY", None)

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

def get_api_key_from_db():
    try:
        conn = mysql.connector.connect(
            host="shortline.proxy.rlwy.net",
            user="root",
            password="bAYeeoxZVEbcpHCPnnDEQPxUomGPPiFI",
            database="railway",
            port=21566
        )
        cursor = conn.cursor()
        cursor.execute("SELECT ApiKey FROM DataWebsiteAI ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        return row[0] if row else None
    except mysql.connector.Error as err:
        print(f"[❗] Database error: {err}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def generate_mock_questions(prompt, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[❗] Error during Gemini API request: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python MockQuestionGenerator.py <subject> <topic1,topic2,...> <difficulty> <question_type1,question_type2,...> <num_questions>")
        sys.exit(1)

    subject = sys.argv[1]
    topics = sys.argv[2].split(',')
    difficulty = sys.argv[3]
    question_types = sys.argv[4].split(',')
    #numQuestions = sys.argv[5]
    try:
        num_questions = int(sys.argv[5])
    except ValueError:
        print("[❗] Number of questions must be an integer.")
        sys.exit(1)

    prompt = f"Subject: {subject}\n"
    prompt += "Topics:\n" + "\n".join(topics) + "\n"
    prompt += f"Question Types: {', '.join(question_types)}\n"
    prompt += f"Number of Questions: {num_questions}\n"
    prompt += f"Difficulty: {difficulty}\n"
    prompt += "Include answers for each question.\n"
    prompt += "Return questions in **Markdown** format with proper formatting.\n"

    api_key = get_api_key_from_db()
    if api_key:
        questions = generate_mock_questions(prompt, api_key)
        if questions:
            print(f"\n[✅] Generated Questions:\n{questions}")
        else:
            print("[⚠️] Failed to generate questions.")
    else:
        print("[❌] API key not found.")
