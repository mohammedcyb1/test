from flask import Flask, request, jsonify, abort
import sqlite3
import os
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load secret key securely from environment variable
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-secret")

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

    # Secure parameterized query
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

    # Secure parameterized query
    cursor.execute(
        "SELECT * FROM products WHERE name LIKE ?",
        (f"%{keyword}%",)
    )

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify(results)


@app.route("/read")
def read_file():
    filename = request.args.get("file", "")

    # Prevent path traversal
    safe_name = secure_filename(filename)

    file_path = os.path.join(UPLOAD_FOLDER, safe_name)

    abs_folder = os.path.abspath(UPLOAD_FOLDER)
    abs_file = os.path.abspath(file_path)

    if not abs_file.startswith(abs_folder):
        abort(403, "Access denied")

    if not os.path.exists(abs_file):
        abort(404, "File not found")

    with open(abs_file, "r", encoding="utf-8") as f:
        content = f.read()

    return jsonify({"content": content})


@app.route("/delete", methods=["POST"])
def delete_user():
    user_id = request.form.get("id", "")

    # Simple authorization example
    is_admin = request.headers.get("X-Admin") == "true"

    if not is_admin:
        abort(403, "Admin access required")

    if not user_id.isdigit():
        abort(400, "Invalid user ID")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Secure parameterized query
    cursor.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "User deleted"})


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400


@app.errorhandler(403)
def forbidden(error):
    return jsonify({"error": str(error)}), 403


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error)}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    # Debug disabled for security
    app.run(host="127.0.0.1", port=5000, debug=False)
