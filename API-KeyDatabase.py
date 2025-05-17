import sys
import mysql.connector


name = sys.argv[1]
apikey = sys.argv[2]

try:
    conn = mysql.connector.connect(
        host="shortline.proxy.rlwy.net",
        user="root",
        password="bAYeeoxZVEbcpHCPnnDEQPxUomGPPiFI",
        database="railway",
        port=21566
    )

    cursor = conn.cursor()

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DataWebsiteAI (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            apikey VARCHAR(255)
        )
    ''')

   
    cursor.execute("INSERT INTO DataWebsiteAI (name, apikey) VALUES (%s, %s)", (name, apikey))
    conn.commit()

    print("success")  

except mysql.connector.Error as err:
    print(f"Database error: {err}", file=sys.stderr)  
    print("fail")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
