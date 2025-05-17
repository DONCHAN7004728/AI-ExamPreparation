import mysql.connector
import google.generativeai as genai
import sys
from datetime import datetime

# ------------------------ DB Connection --------------------------
def connect_to_db():
    return mysql.connector.connect(
        host="shortline.proxy.rlwy.net",
        user="root",
        password="bAYeeoxZVEbcpHCPnnDEQPxUomGPPiFI",
        database="railway",
        port=21566
    )

# ------------------------ Fetch API Key --------------------------
def get_api_key_from_db():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT ApiKey FROM DataWebsiteAI ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        return row[0] if row else None
    except mysql.connector.Error as err:
        print(f"[❗] Database error: {err}")
        return None
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

# ------------------------ CLI Arguments --------------------------
if len(sys.argv) < 5:
    print("Usage: script.py <SubjectName> <Topic> <Date> <DailyStudyHRS>")
    sys.exit(1)

SubjectName = sys.argv[1]
Topic = sys.argv[2]
Date = sys.argv[3]
DailyStudyHRS = sys.argv[4]

# ------------------------ Generate Study Plan --------------------------
def generate_study_timetable(subject, topics, exam_date_str, daily_study_hrs, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-1.5-flash')

        exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d").date()
        today = datetime.today().date()
        total_days = (exam_date - today).days

        if total_days <= 0:
            return "❗ Error: Exam date must be in the future."

        topic_list = [t.strip() for t in topics.split('\n') if t.strip()]
        if not topic_list:
            return "❗ Error: No valid topics provided."

        prompt = f"""
You are a smart study planner.

Create a personalized day-wise study timetable for a student with the following details:

📘 Subject: {subject}
📅 Today's Date: {today}
🧪 Exam Date: {exam_date_str}
📆 Total Days to Prepare: {total_days}
⏰ Daily Study Hours: {daily_study_hrs}
📝 Topics (one per line):
{topics}

Instructions:
- Distribute topics intelligently across the available days.
- Ensure every day has a clear list of topics.
- Include revision days if possible.
- Format the output with dates and bullet points.
- Keep the plan concise and helpful.
"""

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print(f"[❗] Error during Gemini API request: {e}")
        return None

# ------------------------ Execution --------------------------
api_key = get_api_key_from_db()
if not api_key:
    print("[❗] No API key found in the database.")
    sys.exit(1)

result = generate_study_timetable(SubjectName, Topic, Date, DailyStudyHRS, api_key)

# ------------------------ Output --------------------------
if result:
    print(f"TimeTable:\n{result}")
else:
    print("[❗] Summary generation failed.")
