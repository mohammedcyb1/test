import sqlite3
import bcrypt
import secrets
import subprocess
from pathlib import Path

# ✅ Secure password hashing
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)


# ✅ Secure login (NO SQL Injection)
def login(username, password, db_path="users.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )

    result = cursor.fetchone()
    conn.close()

    if result and check_password(password, result[0]):
        return True
    return False


# ✅ Secure random token
def generate_token():
    return secrets.token_hex(16)


# ✅ Safe file reading (protect from path traversal)
def read_file_safe(filename):
    base_dir = Path("files").resolve()
    file_path = (base_dir / filename).resolve()

    if not str(file_path).startswith(str(base_dir)):
        raise ValueError("Access denied")

    with open(file_path, "r") as f:
        return f.read()


# ✅ Safe command execution
def run_command_safe(command):
    allowed_commands = ["echo", "ls"]

    if command[0] not in allowed_commands:
        raise ValueError("Command not allowed")

    subprocess.run(command, check=True)


# ✅ Input validation
def register_user(username, password):
    if not username or len(username) < 3:
        raise ValueError("Invalid username")

    if not password or len(password) < 6:
        raise ValueError("Weak password")

    hashed = hash_password(password)

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed)
    )

    conn.commit()
    conn.close()


# ✅ Clean code (no duplication)
def add_numbers(a, b):
    return a + b


# ✅ Simple and readable function
def process_value(x):
    if x <= 0:
        return 0

    if x < 10 and x % 2 == 0:
        return x * 2

    return x


print("✅ Application running safely")
``
