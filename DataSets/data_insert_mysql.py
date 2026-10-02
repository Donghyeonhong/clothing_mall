import pandas as pd
import mysql.connector

from dotenv import load_dotenv
import os

# CSV 파일
csv_path = r"C:\Users\ooooo\OneDrive\Desktop\졸업작품\데이터셋\clothing_products.csv"

# CSV 읽기
df = pd.read_csv(csv_path)
df = df.astype(object).where(pd.notna(df), None)

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

# 데이터 삽입 SQL
sql = """
INSERT INTO product (
    product_id,
    gender,
    master_category,
    sub_category,
    article_type,
    base_colour,
    season,
    release_year,
    usage_type,
    product_name
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# DataFrame → 튜플
data = [tuple(row) for row in df.itertuples(index=False, name=None)]

# 일괄 삽입
cursor.executemany(sql, data)

conn.commit()

print(f"{cursor.rowcount}개의 데이터가 삽입되었습니다.")

cursor.close()
conn.close()

print(len(df))