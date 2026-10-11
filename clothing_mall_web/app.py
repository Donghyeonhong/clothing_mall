from flask import Flask, render_template, request, flash, redirect, url_for   
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

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
    sql = """select product_name, price, image_url, product.product_id from product inner join
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
    
@app.route("/cart/add", methods=["POST"])
def add_to_cart():
    product_id = request.form.get("product_id", type=int)
    size = request.form.get("size")
    quantity = request.form.get("quantity", type=int)

    if quantity is None:
        flash("올바른 수량을 입력해주세요.")
        return redirect(url_for("product_detail_page", product_id=product_id))
    elif quantity < 1:
        flash("수량이 최소 1개이상이어야 합니다.")
        return redirect(url_for("product_detail_page", product_id=product_id))

    sql = """select option_id from product_option where product_id = %s and size = %s"""
    vals = (product_id, size)

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
            option_result = cursor.fetchone()
            if option_result is None:
                flash("선택한 사이즈의 옵션을 찾을 수 없습니다.")
                return redirect(url_for("product_detail_page", product_id=product_id))
            else:
                option_id = option_result[0]
                sql = """select Quantity from cart where member_id = %s and option_id = %s"""
                vals = (1, option_id)

                cursor.execute(sql, vals)
                cart_result = cursor.fetchone()
                if cart_result is None:
                    sql = """insert into cart (member_id, option_id, Quantity) values (%s, %s, %s)"""
                    vals = (1, option_id, quantity)
                    cursor.execute(sql,vals)
                    conn.commit()
                else:
                    sql = """update cart set Quantity = Quantity + %s where member_id = %s and option_id = %s"""
                    vals = (quantity, 1, option_id)
                    cursor.execute(sql,vals)
                    conn.commit()
        finally:
            if cursor is not None:
                cursor.close()
    finally:
        if conn is not None:
            conn.close()
    flash("성공!")
    return redirect(url_for("product_detail_page", product_id=product_id))    
            


if __name__ == "__main__":
    app.run(debug=True)