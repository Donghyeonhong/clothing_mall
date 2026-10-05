import mysql.connector
import random
from datetime import datetime, timedelta

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

cursor = conn.cursor()

sql = """
UPDATE mall_member SET sign_up_date = %s WHERE member_id = %s
"""

for i in range(1, 7001):
    signupdate = datetime(2025, 9, 23) - timedelta(days=random.randint(0,30))

    vals = (signupdate, i)
    cursor.execute(sql, vals)

conn.commit()