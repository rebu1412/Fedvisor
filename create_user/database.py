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
def add_admin_info(title, content):
    conn = sqlite3.connect("data/data.db")
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO admin_info (title, content, created_at) VALUES (?, ?, ?)", 
        (title, content, created_at)
    )
    
    conn.commit()
    conn.close()

# Lấy danh sách thông tin hành chính
def get_admin_info():
    conn = sqlite3.connect("data/data.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT info_id, title, content, created_at FROM admin_info ORDER BY created_at DESC")
    data = cursor.fetchall()
    
    conn.close()
    return data


# Cập nhật thông tin hành chính
def update_admin_info(info_id, title, content):
    conn = sqlite3.connect("data/data.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE admin_info SET title = ?, content = ? WHERE info_id = ?", 
        (title, content, info_id)
    )
    
    conn.commit()
    conn.close()


# Xóa thông tin hành chính
def delete_admin_info(info_id):
    conn = sqlite3.connect("data/data.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM admin_info WHERE info_id = ?", (info_id,))
    
    conn.commit()
    conn.close()

