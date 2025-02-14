import sqlite3
import hashlib
from datetime import datetime

def connect_db():
    return sqlite3.connect("data/data.db", check_same_thread=False)

# Tạo tài khoản mới
def create_user(username, password, role, user_code, name, email, major):
    conn = connect_db()
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
    conn = connect_db()
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
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM admin_info WHERE info_id = ?", (info_id,))
    
    conn.commit()
    conn.close()


# Thêm công việc mới
def add_job(title, company, requirements, salary, job_type, job_code):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs (title, company, requirements, salary, job_type, job_code) VALUES (?, ?, ?, ?, ?, ?)",
                   (title, company, requirements, salary, job_type, job_code))
    conn.commit()
    conn.close()

# Lấy danh sách công việc
def get_jobs():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT job_id, title, company, requirements, salary, job_type, created_at, job_code FROM jobs ORDER BY created_at DESC")
    jobs = cursor.fetchall()
    conn.close()
    return jobs

# Cập nhật thông tin công việc (bao gồm cả mã công việc)
def update_job(job_id, title, company, requirements, salary, job_type, job_code):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE jobs SET title=?, company=?, requirements=?, salary=?, job_type=?, job_code=? WHERE job_id=?",
                   (title, company, requirements, salary, job_type, job_code, job_id))
    conn.commit()
    conn.close()

# Xóa công việc
def delete_job(job_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE job_id=?", (job_id,))
    conn.commit()
    conn.close()


def add_news(author, title, category, content):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO news (author, title, category, content, status) 
        VALUES (?, ?, ?, ?, 'pending')
    """, (author, title, category, content))
    conn.commit()
    conn.close()

def get_news():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news ORDER BY created_at DESC")
    data = cursor.fetchall()
    conn.close()
    return data

def get_approved_news():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news WHERE status='approved' ORDER BY created_at DESC")
    data = cursor.fetchall()
    conn.close()
    return data

def update_news(news_id, author, title, category, content, status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE news 
        SET author=?, title=?, category=?, content=?, status=? 
        WHERE id=?
    """, (author, title, category, content, status, news_id))
    conn.commit()
    conn.close()

def delete_news(news_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM news WHERE id=?", (news_id,))
    conn.commit()
    conn.close()