import mysql.connector
import random

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
INSERT INTO wishlist(
    member_id,
    product_id
)
VALUES (%s, %s)
"""

cursor.execute("""select product_id from product""")
All_product_id = cursor.fetchall()
# 회원 7000명의 찜 여부와 찜 한 상품 갯수 삽입
for i in range(1, 7001):
    used_product_id = set()
    if random.choice([True, False]):
        for e in range(random.randint(1,7)):
            while True:
                random_product_id = random.choice(All_product_id)
                product_id = random_product_id[0]
                if product_id not in used_product_id:
                    used_product_id.add(product_id)
                    break
            vals = (i, product_id)
            cursor.execute(sql, vals)
    else:
        continue

conn.commit()

