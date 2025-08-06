from flask import Flask, render_template,request,redirect
import sqlite3
from scraper import fetch_case_data

app = Flask(__name__)

def log_query(case_type, case_no, year, raw_html):
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS logs (case_type TEXT, case_no TEXT, year TEXT, raw_html TEXT)")
    c.execute("INSERT INTO logs VALUES (?, ?, ?, ?)", (case_type, case_no, year, raw_html))
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        case_type = request.form["case_type"]
        case_no = request.form["case_no"]
        year = request.form["year"]
        try:
            result, raw_html = fetch_case_data(case_type, case_no, year)
            log_query(case_type, case_no, year, raw_html)
            return render_template("result.html", result=result)
        except Exception as e:
            return f"<h3>Error: {str(e)}</h3>"
    return render_template("index.html")
