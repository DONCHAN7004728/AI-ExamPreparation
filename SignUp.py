import sys
import mysql.connector


name = sys.argv[1]
email = sys.argv[2]
password = sys.argv[3]


conn = mysql.connector.connect(
    host="caboose.proxy.rlwy.net",
    user="root",
    password="kSFCjWBLJRtYdCvlbnoGYbrvhiwiBXso",
    database="railway",
    port=33995
)

cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
)
''')

try:
    cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
    conn.commit()
    print("User added successfully.")
except mysql.connector.IntegrityError:
    print("Email already exists.")
    sys.exit(1)


cursor.close()
conn.close()
sys.exit(0)
