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

sql = """ 
INSERT INTO order_detail(
    order_id,
    option_id,
    Quantity,
    unit_price 
)
VALUES (%s, %s, %s, %s)
"""

# 주문번호 5번부터 17472번까지의 더미 주문세부 데이터 삽입
for i in range(5, 17473):
    used_option_id = set()
    for e in range(1, random.randint(3,4)):
        while True:
            if random.choice([True, False]):
                option_id = random.randint(2, 83045)
            else:
                option_id = random.randint(135167, 135805)
        
            if option_id not in used_option_id:
                used_option_id.add(option_id)    
                break   
        cursor.execute("""select price from product inner join product_option on product.product_id = product_option.product_id where product_option.option_id = %s""", (option_id,))
        price = cursor.fetchone()[0]
        vals = (i, option_id, random.randint(1,3), price)
        cursor.execute(sql, vals)
conn.commit()    