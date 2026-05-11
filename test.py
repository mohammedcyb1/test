import os
import sqlite3

# Hardcoded password (Security issue)
ADMIN_PASSWORD = "123456"


# SQL Injection vulnerability
def login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)

    result = cursor.fetchone()
    conn.close()

    if result:
        return True
    return False


# Command Injection vulnerability
def run_command(user_input):
    os.system("echo " + user_input)


# Bad practice: using global variables
global_data = []

def add_data(value):
    global global_data
    global_data.append(value)


# Weak randomness (security issue)
import random
def generate_token():
    return random.randint(1000, 9999)


# Bug: type error
def calculate_total():
    price = 100
    tax = "15"
    return price + tax   # BUG


# Hardcoded file path (bad practice)
def read_secret():
    with open("/etc/passwd", "r") as f:
        return f.read()


# No input validation (security issue)
def register_user(username, password):
    if len(username) < 2:
        return "Too short"

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO users VALUES ('{username}', '{password}')")
    conn.commit()
    conn.close()


# Code smell: duplicated code
def calc1():
    a = 5
    b = 10
    return a + b

def calc2():
    a = 5
    b = 10
    return a + b


# Very complex function (complexity issue)
def messy_function(x):
    if x > 0:
        if x < 10:
            if x % 2 == 0:
                if x > 5:
                    return x * 2
                else:
                    return x + 1
            else:
                return x - 1
        else:
            return x * 10
    else:
        return 0


print("Done")
