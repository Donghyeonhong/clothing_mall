from flask import Flask, render_template
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

sql = """select product_name, price, image_url, product.product_id from product inner join product_image on product.product_id = product_image.product_id limit 20"""

@app.route("/")
def home():
    conn = None
    try:
        # mysql 연결
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password=os.getenv("DB_PASSWORD"),
            database="clothing_mall"
            )
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            products = cursor.fetchall()
        finally:
            if cursor is not None:
                cursor.close()
    finally:
        if conn is not None:
            conn.close()
    return render_template("index.html", products = products)

@app.route("/product/<int:product_id>")
def product_detail_page(product_id):
    sql = """select product_name, price, image_url from product inner join
        product_image on product.product_id = product_image.product_id 
        where product.product_id = %s"""
    
    vals = (product_id,)

    conn = None
    try:
        # mysql 연결
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password=os.getenv("DB_PASSWORD"),
            database="clothing_mall"
            )
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(sql, vals)
            product_detail = cursor.fetchone()
        finally:
            if cursor is not None:
                cursor.close()
    finally:
        if conn is not None:
            conn.close()
    return render_template('product_detail.html', product_detail = product_detail)
    

if __name__ == "__main__":
    app.run(debug=True)