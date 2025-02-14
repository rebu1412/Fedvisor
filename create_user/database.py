import sqlite3
import hashlib
from datetime import datetime

# Tạo tài khoản mới
def create_user(username, password, role, user_code, name, email, major):
    conn = sqlite3.connect("data/data.db")
    cursor = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    try:
        cursor.execute("""
            INSERT INTO users (username, password_hash, role, user_code, name, email, major)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, password_hash, role, user_code, name, email, major))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Kiểm tra đăng nhập
def check_login(username, password):
    conn = sqlite3.connect("data/data.db")
    cursor = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, password_hash))
    user = cursor.fetchone()
    conn.close()
    return user

# Thêm thông tin hành chính với ID tự động tăng
def add_admin_info(title, content, topic):
    with sqlite3.connect("data/data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO admin_info (title, content, topic, created_at) VALUES (?, ?, ?, datetime('now'))",
                       (title, content, topic))
        conn.commit()

# Lấy danh sách thông tin hành chính
def get_admin_info():
    with sqlite3.connect("data/data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT info_id, title, content, topic, created_at FROM admin_info ORDER BY created_at DESC")
        return cursor.fetchall()


# Cập nhật thông tin hành chính
def update_admin_info(info_id, new_title, new_content, new_topic):
    with sqlite3.connect("data/data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE admin_info SET title = ?, content = ?, topic = ? WHERE info_id = ?",
                       (new_title, new_content, new_topic, info_id))
        conn.commit()


# Xóa thông tin hành chính
def delete_admin_info(info_id):
    conn = sqlite3.connect("data/data.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM admin_info WHERE info_id = ?", (info_id,))
    
    conn.commit()
    conn.close()
