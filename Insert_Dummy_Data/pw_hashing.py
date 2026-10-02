import bcrypt
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

cursor = conn.cursor()

# 회원 테이블 데이터 삽입구문
sql = """
INSERT INTO mall_member(
    login_id,
    login_password,
    member_name,
    email,
    phone_number
)
VALUES (%s, %s, %s, %s, %s)
"""
password = 'test1234'.encode("utf-8")

# 회원 데이터 삽입
for i in range(6,7001):
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())  # 비밀번호 해싱
    vals = ("testid" + str(i), hashed.decode("utf-8"), "test" + str(i), "testid" + str(i) + "@gmail.com", "010-0000-" + str(i).zfill(4)) 
    cursor.execute(sql, vals)

# 변경사항 확정
conn.commit()
