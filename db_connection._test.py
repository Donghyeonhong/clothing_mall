import mysql.connector

from dotenv import load_dotenv
import os

load_dotenv()

# mysql 연결
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password=os.getenv("DB_PASSWORD"),
    database="clothing_mall"
)

if conn.is_connected():
    print("MySQL 연결 성공")
    conn.close()