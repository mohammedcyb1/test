import sqlite3
import secrets


# ✅ إنشاء اتصال بقاعدة البيانات
def get_connection():
    return sqlite3.connect("users.db")


# ✅ إضافة مستخدم (مع حماية من SQL Injection)
def register_user(username, password):
    if not username or len(username) < 3:
        raise ValueError("Invalid username")

    if not password or len(password) < 6:
        raise ValueError("Weak password")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )

    conn.commit()
    conn.close()


# ✅ تسجيل الدخول
def login(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    )

    result = cursor.fetchone()
    conn.close()

    return result is not None


# ✅ توليد رمز آمن
def generate_token():
    return secrets.token_hex(16)


# ✅ دالة بسيطة نظيفة
def add_numbers(a, b):
    return a + b


# ✅ تشغيل البرنامج
def main():
    token = generate_token()
    print("Token:", token)

    result = add_numbers(5, 10)
    print("Result:", result)


if __name__ == "__main__":
    main()
``
