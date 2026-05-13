from flask import Flask, request, jsonify, abort
import sqlite3
import subprocess
import os
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
DATABASE = "users.db"
UPLOAD_FOLDER = "files"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Safe parameterized query
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user["password"], password):
        return jsonify({"message": "Login successful"})

    return jsonify({"message": "Invalid username or password"}), 401


@app.route("/search")
def search():
    keyword = request.args.get("q", "")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Safe parameterized query
    cursor.execute(
        "SELECT * FROM products WHERE name LIKE ?",
        (f"%{keyword}%",)
    )

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify(results)


@app.route("/ping")
def ping():
    host = request.args.get("host", "")

    # Basic input validation
    if not host.replace(".", "").replace("-", "").isalnum():
        abort(400, "Invalid host")

    # Avoid shell=True
    result = subprocess.check_output(
        ["ping", "-c", "1", host],
        text=True,
        timeout=5
    )

    return jsonify({"result": result})


@app.route("/read")
def read_file():
    filename = request.args.get("file", "")
    safe_name = secure_filename(filename)

    file_path = os.path.join(UPLOAD_FOLDER, safe_name)
    abs_folder = os.path.abspath(UPLOAD_FOLDER)
    abs_file = os.path.abspath(file_path)

    # Prevent path traversal
    if not abs_file.startswith(abs_folder):
        abort(403, "Access denied")

    if not os.path.exists(abs_file):
        abort(404, "File not found")

    with open(abs_file, "r", encoding="utf-8") as f:
        content = f.read()

    return jsonify({"content": content})


@app.route("/delete", methods=["POST"])
def delete_user():
    user_id = request.form.get("id")

    # Example simple authorization check
    is_admin = request.headers.get("X-Admin") == "true"

    if not is_admin:
        abort(403, "Admin access required")

    if not user_id or not user_id.isdigit():
        abort(400, "Invalid user ID")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "User deleted"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
