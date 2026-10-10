import pandas as pd
import mysql.connector

from dotenv import load_dotenv
import os

# CSV 파일
csv_path = r"C:\clothing_mall\DataSets\cloth_image.csv"

# CSV 읽기
df = pd.read_csv(csv_path)
df = df.astype(object).where(pd.notna(df), None)

product_id = (
    df["filename"]
    .str.replace(".jpg", "", regex=False)
    .astype(int)
)

image_url = df["link"]

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

sql = """insert into product_image(product_id, image_url) 
values (%s, %s)"""



vals = list(zip(product_id, image_url))  


# 일괄 삽입
cursor.executemany(sql, vals)

conn.commit()

print(f"{cursor.rowcount}개의 데이터가 삽입되었습니다.")

cursor.close()
conn.close()

print(len(df))
