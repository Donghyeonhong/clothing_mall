import mysql.connector
import random
from datetime import datetime, timedelta

# mysql 연결
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="REDACTED_PASSWORD",
    database="clothing_mall"
)

cursor = conn.cursor()

sql = """ 
INSERT INTO product_order(
    member_id,
    order_date
)
VALUES (%s, %s)
"""

for i in range(11, 7001):   # 회원 10명 주문 + 11번 회원부터 7000번 회원까지의 주문
    for t in range(1, random.randint(3,4)):   # 최근 1년 내 1명당 2~3건의 주문
        vals = (i, datetime.now() - timedelta(days=random.randint(0,365)))
        cursor.execute(sql, vals)

conn.commit()
