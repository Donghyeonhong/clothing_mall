from flask import Flask, render_template, request, flash, redirect, url_for   
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="clothing_mall"
    )

@app.route("/")
def home():
    conn = None
    try:
        # mysql 연결
        conn = get_db_connection()
        cursor = None
        try:
            category = request.args.get('category', 'all')
            page = request.args.get('page', 1, type=int)
            offset = (page - 1) * 20
            cursor = conn.cursor()
            sql= """select product_name, price, image_url, product.product_id from product inner join product_image on product.product_id = product_image.product_id"""
            product_count = """select count(*) from product inner join product_image on product.product_id = product_image.product_id"""

            if category == 'all':
                condition = """"""
            elif category == 'Topwear':
                condition = """ where sub_category = 'Topwear' and article_type not in('Jackets', 'Blazers', 'Rain Jacket', 'Nehru Jackets', 'Waistcoat', 'Shrug')"""
            elif category == 'Bottomwear':
                condition = """ where sub_category = 'Bottomwear' and article_type not in('Swimwear', 'Skirts', 'Stockings', 'Tights', 'Tracksuits', 'Salwar and Dupatta')"""
            elif category == 'Outerwear':
                condition = """ where article_type in ('Jackets', 'Blazers', 'Rain Jacket', 'Nehru Jackets', 'Waistcoat', 'Shrug')"""
            else:
                condition = """ where sub_category not in ('Topwear', 'Bottomwear') or article_type in ('Swimwear', 'Skirts', 'Stockings', 'Tights', 'Tracksuits', 'Salwar and Dupatta')""" 

            sql = sql + condition + f""" limit {offset}, 20"""
            product_count = product_count + condition

            cursor.execute(sql)
            products = cursor.fetchall()

            cursor.execute(product_count)
            count_result = cursor.fetchone()
            total_pages = (count_result[0] + 19) // 20
            start_page = ((page - 1) // 5) * 5 + 1
            end_page = min(start_page+4, total_pages)
        finally:
            if cursor is not None:
                cursor.close()
    finally:
        if conn is not None:
            conn.close()
    return render_template("index.html", products = products, product_count=count_result[0], page=page, total_pages=total_pages, start_page=start_page, end_page=end_page)

@app.route("/product/<int:product_id>")
def product_detail_page(product_id):
    sql = """select product_name, price, image_url, product.product_id from product inner join
        product_image on product.product_id = product_image.product_id 
        where product.product_id = %s"""
    
    vals = (product_id,)

    conn = None
    try:
        # mysql 연결
        conn = get_db_connection()
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
        conn = get_db_connection()
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