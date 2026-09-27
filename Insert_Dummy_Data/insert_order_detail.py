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


            