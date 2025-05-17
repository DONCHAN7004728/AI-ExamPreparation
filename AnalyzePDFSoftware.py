import sys
import os
import codecs
import mysql.connector
import google.generativeai as genai
import PyPDF2

# Remove proxy settings (for environments like Railway)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("HTTP_PROXY", None)

# Set UTF-8 output encoding
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

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

def analyze_pdf(pdf_path, analysis_type, include_examples, include_definitions, format_type, api_key):
    try:
        reader = PyPDF2.PdfReader(pdf_path)
        text = "".join([page.extract_text() for page in reader.pages])
        
        prompt = f"Analyze this text:\n{text}\n\n"
        prompt += f"Analysis Type: {analysis_type}\n"
        if include_examples:
            prompt += "Include relevant examples.\n"
        if include_definitions:
            prompt += "Include key definitions.\n"
        if format_type.lower() == "markdown":
            prompt += "Format the analysis using Markdown (headings, lists, emphasis, etc.).\n"
        else:
            prompt += "Generate the analysis in plain text format without any Markdown formatting.\n"
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)

        return response.text.strip()
    except Exception as e:
        print(f"[❗] Error during PDF analysis: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python AnalyzePDFSoftware.py <pdf_path> <analysis_type> <include_examples:yes/no> <include_definitions:yes/no> <format:markdown/plain>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    analysis_type = sys.argv[2]
    include_examples = sys.argv[3].lower() == "yes"
    include_definitions = sys.argv[4].lower() == "yes"
    format_type = sys.argv[5]

    if not os.path.exists(pdf_path):
        print(f"[❌] File not found: {pdf_path}")
        sys.exit(1)

    api_key = get_api_key_from_db()

    if api_key:
        result = analyze_pdf(pdf_path, analysis_type, include_examples, include_definitions, format_type, api_key)
        if result:
            print(f"[✅] Analysis Result:\n\n{result}")
        else:
            print("[⚠️] No analysis result returned.")
    else:
        print("[❌] API key not found.")
