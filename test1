import os
import sqlite3
import random
import hashlib
import pickle

password = "123"   # 🔴 hardcoded password


# 🔴 authentication bypass + logic error
def login(user, pwd):
    if user == "admin":
        return True

    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username = '" + user + "' AND password = '" + pwd + "'"
    cursor.execute(query)

    return cursor.fetchone()


# 🔴 SQL Injection
def get_user(id):
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=" + id)


# 🔴 command injection
def run_cmd(cmd):
    os.system(cmd)


# 🔴 path traversal
def read_file(name):
    f = open("../../" + name)
    data = f.read()
    return data


# 🔴 insecure deserialization
def load_data(file):
    with open(file, "rb") as f:
        return pickle.load(f)


# 🔴 weak hashing
def hash_pwd(p):
    return hashlib.md5(p.encode()).hexdigest()


# 🔴 weak random
def token():
    return str(random.random())


# 🔴 bug (crash)
def calc():
    a = 10
    b = "20"
    return a + b


# 🔴 duplicated code
def sum1():
    x = 5
    y = 10
    return x + y

def sum2():
    x = 5
    y = 10
    return x + y


# 🔴 global variable misuse
global_counter = 0

def inc():
    global global_counter
    for i in range(1000):
        global_counter += 1


# 🔴 no input validation
def register(username, password):
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users VALUES ('" + username + "','" + password + "')")
    conn.commit()


# 🔴 extremely bad complexity
def messy(x):
    if x > 0:
        if x < 10:
            if x % 2 == 0:
                if x > 5:
                    if x > 7:
                        if x > 8:
                            return x*4
                        else:
                            return x*3
                    else:
                        return x*2
                else:
                    return x+1
            else:
                return x-1
        else:
            return x*10
    else:
        return 0


# 🔴 sensitive data exposure
def show_env():
    return os.environ


# 🔴 dangerous delete
def delete_everything():
    os.system("rm -rf /")


print("Running app...")
``
