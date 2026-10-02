import mysql.connector
import random
from datetime import timedelta

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
INSERT INTO review(
    member_id,
    product_id,
    review_score,
    review_content,
    review_date
)
VALUES (%s, %s, %s, %s, %s)
"""

cursor = conn.cursor()

for i in range(1, 7001):
    if random.choice([True, False, False, False, False]):
        cursor.execute("""select product_id, min(order_date) from product_option inner join order_detail on product_option.option_id = order_detail.option_id inner join product_order on order_detail.order_id = product_order.order_id where product_order.member_id = %s group by product_id""", (i,))     #조인연결

        purchase_product = cursor.fetchall()  #회원이 주문한 상품번호, 최초 주문일 목록 추출

        used_product_id = set()
        review_count = random.randint(1,2)  # r은 리뷰 횟수

        for e in range(min(len(purchase_product), review_count)):
            while True:
                random_product = random.choice(purchase_product)
                product_id = random_product[0]
                if product_id not in used_product_id:
                    used_product_id.add(product_id)
                    break

            review_score = random.randint(10, 50) / 10
            if review_score >= 1 and review_score < 2:
                content = "만족하지 못 했습니다."
            elif review_score >=2 and review_score < 4:
                content = "보통입니다."
            else:
                content = "만족합니다."

            order_date = random_product[1]
            review_date = order_date + timedelta(days=random.randint(0,30))
            vals = (i, product_id, review_score, content, review_date)
            cursor.execute(sql, vals)
conn.commit()


