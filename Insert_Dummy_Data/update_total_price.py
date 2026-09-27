import mysql.connector
import random

# mysql 연결
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="REDACTED_PASSWORD",
    database="clothing_mall"
)

cursor = conn.cursor()

# 주문 테이블의 주문번호별 총 금액 업데이트
sql = """ 
UPDATE product_order SET total_price = (SELECT SUM(unit_price * Quantity) FROM order_detail WHERE order_id = %s) WHERE order_id = %s
"""

for i in range(1, 17473):
    vals = (i, i)
    cursor.execute(sql, vals)

conn.commit()