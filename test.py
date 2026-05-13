from flask import Flask, request
import sqlite3
import subprocess
import pickle
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "123456"
DB_PASSWORD = "admin123"
API_KEY = "sk_test_123456789"

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    cursor.execute(query)

    user = cursor.fetchone()

    if user:
        return "Login successful"
    else:
        return "Invalid username or password"

@app.route("/search")
def search():
    keyword = request.args.get("q")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE name LIKE '%" + keyword + "%'")
    results = cursor.fetchall()

    return str(results)

@app.route("/ping")
def ping():
    host = request.args.get("host")

    result = subprocess.check_output("ping -c 1 " + host, shell=True)

    return result

@app.route("/load")
def load_data():
    data = request.args.get("data")

    obj = pickle.loads(bytes(data, "utf-8"))

    return str(obj)

@app.route("/read")
def read_file():
    filename = request.args.get("file")

    with open(filename, "r") as f:
        content = f.read()

    return content

@app.route("/debug")
def debug():
    return str(os.environ)

@app.route("/delete")
def delete_user():
    user_id = request.args.get("id")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = " + user_id)
    conn.commit()

    return "User deleted"

if __name__ == "__main__":
    # Debug mode enabled in production
    app.run(host="0.0.0.0", port=5000, debug=True)
