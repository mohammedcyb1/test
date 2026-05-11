import os
import pickle
import sqlite3
import hashlib
import subprocess

# 🔴 Hardcoded secret key
SECRET_KEY = "super_secret_key_123"

# 🔴 Weak hashing (MD5)
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


# 🔴 Authentication bypass (logic flaw)
def authenticate(username, password):
    if username == "admin":
        return True  # BUG 🚨

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
    result = cursor.fetchone()

    conn.close()
    return result is not None


# 🔴 SQL Injection again
def get_user_data(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)

    data = cursor.fetchall()
    conn.close()
    return data


# 🔴 Command Injection
def delete_file(filename):
    os.system("rm -rf " + filename)


# 🔴 Insecure deserialization (خطير جدًا)
def load_user_session(file):
    with open(file, "rb") as f:
        return pickle.load(f)  # 🚨 ممكن تنفيذ كود ضار


# 🔴 Path Traversal
def read_file(filename):
    with open("files/" + filename, "r") as f:
        return f.read()


# 🔴 Sensitive data exposure
def print_env():
    return os.environ


# 🔴 Weak random token
import random
def create_token():
    return str(random.random())


# 🔴 Missing auth check
def delete_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id=" + str(user_id))
    conn.commit()
    conn.close()


# 🔴 Race condition (conceptual)
shared_counter = 0

def increment():
    global shared_counter
    for _ in range(1000):
        shared_counter += 1


# 🔴 Code duplication
def sum1():
    a = 1
    b = 2
    return a + b

def sum2():
    a = 1
    b = 2
    return a + b


# 🔴 Bug (crash)
def crash():
    x = 10
    y = "20"
    return x + y


# 🔴 Very complex function
def complex_logic(x):
    if x > 0:
        if x < 10:
            if x % 2 == 0:
                if x > 5:
                    if x > 7:
                        return x * 3
                    else:
                        return x * 2
                else:
                    return x + 1
            else:
                return x - 1
        else:
            return x * 10
    else:
        return 0


print("App running")
``
