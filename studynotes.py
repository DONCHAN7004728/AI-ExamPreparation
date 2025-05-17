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


def generate_study_notes(topic, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-1.5-flash')

        prompt = f"""
        Generate comprehensive study notes on the topic: "{topic}". Include:
        - Key concepts
        - Definitions
        - Real-life applications
        - Summary
        - Important formulas
        - Tips for understanding and remembering the topic
        Format the output in clean markdown.
        """

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[❗] Error during Gemini API request: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python studynotes.py <topic>")
        sys.exit(1)

    topic = sys.argv[1]
    api_key = get_api_key_from_db()

    if api_key:
        notes = generate_study_notes(topic, api_key)
        if notes:
            print(notes)
        else:
            print("[⚠️] No notes generated.")
    else:
        print("[❌] API key not found.")
