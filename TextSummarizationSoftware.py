import mysql.connector
import google.generativeai as genai
import json
import os
import socketserver
from http.server import BaseHTTPRequestHandler
import sys

################################## Connect to DB #####################################
def connect_to_db():
    conn = mysql.connector.connect(
        host="shortline.proxy.rlwy.net",
        user="root",
        password="bAYeeoxZVEbcpHCPnnDEQPxUomGPPiFI",
        database="railway",
        port=21566
    )
    return conn
################################## Connect to DB #####################################

################################## Fetch the API-Key from database ##################
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
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
################################## Fetch the API-Key from database ##################



############################# Input from j-son ########################################
text = sys.argv[1]
summary_length = sys.argv[2]
include_key_points = sys.argv[3]
use_bullet_points = sys.argv[4]
############################# Input from j-son ########################################



################################### Context to ans. #################################
def summarize_story(context, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        

        prompt = f"Please summarize the following story pointWise:\n\n{context}"
        response = model.generate_content(prompt)
        summary = response.text.strip()  
        return summary
    except Exception as e:
        print(f"[❗] Error during Gemini API request: {e}")
        return None
################################### Context to ans. #################################

####################################### Calling all function ######################
api_key = get_api_key_from_db()  
if api_key:
    result = summarize_story(text, api_key)  
else:
    print("[❗] API Key not found.")
    result = None
####################################### Calling all function ######################

############################### For result push data ##################################
if result:
    print(f"Summary: \n{result}")
else:
    print("[❗] Summary generation failed.")
############################### For result push data ##################################
