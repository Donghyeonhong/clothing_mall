from flask import Flask, render_template
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

sql = """select product_name, price from product limit 20"""

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


if __name__ == "__main__":
    app.run(debug=True)