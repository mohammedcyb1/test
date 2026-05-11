import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# ثغرة 1: بيانات حساسة مكشوفة (Hardcoded Secrets)
# Codacy ستعطيك تنبيه أمني فوراً بسبب وجود مفتاح سري في الكود
API_KEY = "12345-ABCDE-98765-ZYXWV"

@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    
    # ثغرة 2: حقن قواعد البيانات (SQL Injection)
    # استخدام f-string في الاستعلام يجعل قاعدة البيانات عرضة للاختراق
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # ثغرة 3: تشغيل أوامر النظام (Command Injection)
    # السماح للمستخدم بتنفيذ أوامر مباشرة على السيرفر
    os.system(f"echo Searching for user {user_id}")
    
    cursor.execute(query)
    return str(cursor.fetchone())

if __name__ == "__main__":
    # ثغرة 4: وضع التطوير (Debug Mode)
    # تشغيل التطبيق في وضع الـ Debug على السيرفر خطر جداً
    app.run(debug=True)
