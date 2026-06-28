import os
import time
import pymysql
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# 載入本地 .env 檔案（如果有的話）
load_dotenv()

app = Flask(__name__)

# 從環境變數讀取資料庫設定，若無設定則使用預設值
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = int(os.environ.get('DB_PORT', 8625))
DB_USER = os.environ.get('MYSQL_USER', 'cki101_user')
DB_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'cki101_password')
DB_NAME = os.environ.get('MYSQL_DATABASE', 'cki101_db')

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    print(f"Initializing database connection to {DB_HOST}:{DB_PORT}...", flush=True)
    # 重試機制：MySQL 容器初次啟動需要時間，在此設定最多重試 15 次，每次間隔 2 秒
    for i in range(15):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        age INT NOT NULL
                    )
                """)
            conn.commit()
            conn.close()
            print("Database table initialization successful!", flush=True)
            return True
        except Exception as e:
            print(f"Database connection attempt {i+1} failed: {e}. Retrying in 2 seconds...", flush=True)
            time.sleep(2)
    print("Could not initialize database. Please check connection config.", flush=True)
    return False

# 於 Flask 應用程式初始化時執行資料庫結構建立
with app.app_context():
    init_db()

@app.route('/')
def home():
    return '我是功能-'

# 頁面路由：渲染前端操作介面
@app.route('/user')
def user_interface():
    return render_template('user.html')

# 使用者 CRUD API 路由
@app.route('/api/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, name, age FROM users")
                result = cursor.fetchall()
            conn.close()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'name' not in data or 'age' not in data:
            return jsonify({"error": "Missing 'name' or 'age' in payload"}), 400
        
        name = data['name']
        try:
            age = int(data['age'])
        except (ValueError, TypeError):
            return jsonify({"error": "'age' must be an integer"}), 400

        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "INSERT INTO users (name, age) VALUES (%s, %s)"
                cursor.execute(sql, (name, age))
                user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return jsonify({
                "message": "User created successfully",
                "id": user_id,
                "name": name,
                "age": age
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 檢查使用者是否存在
            cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                conn.close()
                return jsonify({"error": "User not found"}), 404
            
            # 執行刪除
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": f"User {user_id} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Flask 監聽 5000 port
    app.run(host='0.0.0.0', port=5000)
