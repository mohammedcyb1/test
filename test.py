from flask import Flask, request, jsonify, abort
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "change-this-secret"
)

UPLOAD_FOLDER = "files"

USERS = [
    {
        "id": 1,
        "username": os.environ.get("ADMIN_USERNAME", "admin"),
        "password": os.environ.get("ADMIN_PASSWORD", "")
    },
    {
        "id": 2,
        "username": os.environ.get("NORMAL_USERNAME", "user"),
        "password": os.environ.get("NORMAL_PASSWORD", "")
    }
]

PRODUCTS = [
    {"id": 1, "name": "Laptop"},
    {"id": 2, "name": "Mouse"},
    {"id": 3, "name": "Keyboard"}
]


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    user = next(
        (
            item for item in USERS
            if item["username"] == username
            and item["password"] == password
        ),
        None
    )

    if user:
        return jsonify({"message": "Login successful"})

    return jsonify({"message": "Invalid credentials"}), 401


@app.route("/search")
def search():
    keyword = request.args.get("q", "").lower()

    results = [
        product
        for product in PRODUCTS
        if product["name"].lower() == keyword
    ]

    return jsonify(results)


@app.route("/read")
def read_file():
    filename = request.args.get("file", "")
    safe_name = secure_filename(filename)

    file_path = os.path.join(UPLOAD_FOLDER, safe_name)
    abs_folder = os.path.abspath(UPLOAD_FOLDER)
    abs_file = os.path.abspath(file_path)

    if not abs_file.startswith(abs_folder):
        abort(403)

    if not os.path.isfile(abs_file):
        abort(404)

    with open(abs_file, "r", encoding="utf-8") as file:
        content = file.read()

    return jsonify({"content": content})


@app.route("/delete", methods=["POST"])
def delete_user():
    user_id = request.form.get("id", "")

    is_admin = request.headers.get("X-Admin") == "true"

    if not is_admin:
        abort(403)

    if not user_id.isdigit():
        abort(400)

    return jsonify({"message": "User deleted safely"})


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400


@app.errorhandler(403)
def forbidden(error):
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )


