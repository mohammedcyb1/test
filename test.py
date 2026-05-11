import os
import sqlite3
from flask import Flask, request, abort

app = Flask(__name__)

# 1. حل مشكلة البيانات الحساسة:
# بدلاً من كتابة المفتاح هنا، نسحبه من "متغيرات البيئة" (Environment Variables)
API_KEY = os.getenv("MY_APP_API_KEY")

@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    
    # التأكد من وجود المدخلات لمنع الأخطاء المفاجئة
    if not user_id:
        abort(400, description="Missing user ID")

    # 2. حل ثغرة SQL Injection:
    # نستخدم البارامترات (?) بدلاً من f-string. المحرك سيتكفل بتنقية المدخلات.
    query = "SELECT * FROM users WHERE id = ?"
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # 3. حل ثغرة Command Injection:
    # تجنب استخدام os.system نهائياً مع مدخلات المستخدم. 
    # نستخدم الطباعة العادية داخل لغة البرمجة نفسها.
    print(f"Searching for user {user_id}")
    
 # 1. تعريف الاستعلام باستخدام علامة الاستهام فقط (بدون دمج المتغير في النص)
query = "SELECT * FROM users WHERE id = ?"

# 2. تمرير المتغير كـ Tuple في دالة execute
# هذا هو السطر 32 الذي تعترض عليه الأداة حالياً
cursor.execute(query, (user_id,))
    
    return str(result) if result else "User not found"

if __name__ == "__main__":
    # 4. حل ثغرة Debug Mode:
    # في المشاريع الحقيقية، يجب دائماً تعطيل وضع التصحيح
    app.run(debug=False)
