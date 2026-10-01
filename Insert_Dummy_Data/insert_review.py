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
INSERT INTO review(
    member_id,
    product_id,
    review_score,
    review_content,
    review_date
)
VALUES (%s, %s, %s, %s, %s)
"""

