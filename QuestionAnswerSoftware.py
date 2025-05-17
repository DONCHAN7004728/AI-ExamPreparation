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


def ask_ai_question(question, context, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-1.5-flash')

        prompt = f"Context: {context}\n\nQuestion: {question}" if context else question
        response = model.generate_content(prompt)

        return response.text.strip()
    except Exception as e:
        print(f"[❗] Error during Gemini API request: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python QuestionAnswerSoftware.py <question> <context>")
        sys.exit(1)

    question = sys.argv[1]
    context = sys.argv[2]

    api_key = get_api_key_from_db()

    if api_key:
        answer = ask_ai_question(question, context, api_key)
        if answer:
            print(f"[✅] Answer:\n{answer}")
        else:
            print("[⚠️] No answer found or error during response.")
    else:
        print("[❌] API key not found.")
