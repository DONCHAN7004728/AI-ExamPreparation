import sys
import sqlite3


email = sys.argv[1]
password = sys.argv[2]


conn = sqlite3.connect("users.db")
cursor = conn.cursor()


cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
user = cursor.fetchone()

if user:
    print("valid")  
else:
    print("invalid")  


conn.close()
