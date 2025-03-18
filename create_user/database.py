import sqlite3
import hashlib
from datetime import datetime
import uuid
import streamlit as st


def connect_db():
    return sqlite3.connect("data/data.db", check_same_thread=False)

# Tạo tài khoản mới
def create_user(username, password, role, user_code, name, major):
    conn = connect_db()
    cursor = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    try:
        cursor.execute("""
            INSERT INTO users (username, password_hash, role, user_code, name, major)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, password_hash, role, user_code, name, major))
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

def add_feedback(user_id, topic, content):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO forum_posts (user_id, topic, content) VALUES (?, ?, ?)", (user_id, topic, content))
    conn.commit()
    conn.close()

def get_feedbacks():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.post_id, u.username, f.topic, f.content, f.created_at
        FROM forum_posts f
        JOIN users u ON f.user_id = u.user_id
        ORDER BY f.created_at DESC
    """)
    feedbacks = cursor.fetchall()
    conn.close()
    return feedbacks

def add_comment(user_id, post_id, content):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)", (post_id, user_id, content))
    conn.commit()
    conn.close()

def get_comments(post_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.comment_id, c.post_id, u.username, c.content, c.created_at
        FROM comments c
        JOIN users u ON c.user_id = u.user_id
        WHERE c.post_id = ?
        ORDER BY c.created_at ASC
    """, (post_id,))
    comments = cursor.fetchall()
    conn.close()
    return comments

def delete_feedback(post_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM forum_posts WHERE post_id = ?", (post_id,))
    conn.commit()
    conn.close()

def get_all_users():
    """Lấy danh sách tất cả người dùng từ database"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, password_hash, role FROM users")  # Đảm bảo lấy cả 'role'
    users = cursor.fetchall()
    return users


def track_usage(action):
    """Cập nhật số lần sử dụng của một chức năng, gộp chung 'view_job_*'"""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Nếu action bắt đầu bằng 'view_job_', thì gộp vào nhóm chung 'view_job'
    if action.startswith("view_job_"):
        action = "view_job"  # Đổi tất cả thành 'view_job'

    cursor.execute("INSERT INTO usage_tracking (action, count) VALUES (?, 1) "
                   "ON CONFLICT(action) DO UPDATE SET count = count + 1", (action,))
    
    conn.commit()
    conn.close()

def get_usage_stats():
    """Lấy dữ liệu thống kê và gộp nhóm các mục view_job"""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT action, count FROM usage_tracking")
    data = cursor.fetchall()
    
    conn.close()

    # Định nghĩa tên hiển thị
    action_labels = {
        "chatbot_usage": "Chatbot hành chính",
        "job_chatbot_query": "Chatbot công việc",
        "feedback_submitted": "Feedback",
        "comment_submitted": "Comment",
        "view_job": "Xem thông tin việc làm",
        "user_home": "Đăng nhập"
    }

    # Xử lý dữ liệu
    formatted_data = {}
    job_view_count = 0

    for action, count in data:
        if action.startswith("view_job_"):
            job_view_count += count  # Gộp tất cả 'view_job_*' vào 'view_job'
        else:
            formatted_data[action_labels.get(action, action)] = count

    if job_view_count > 0:
        formatted_data["Xem thông tin việc làm"] = job_view_count

    return formatted_data

def update_user_info(user_id, username, role):
    """Cập nhật thông tin username và role"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username = ?, role = ? WHERE user_id = ?", (username, role, user_id))
    conn.commit()
    conn.close()

def update_user_password(username, new_password):
    """Cập nhật mật khẩu người dùng dựa trên username với mã hóa bảo mật"""
    # Mã hóa mật khẩu mới
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

    conn = connect_db()
    cursor = conn.cursor()

    # Kiểm tra xem username có tồn tại không
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
    if cursor.fetchone()[0] == 0:
        conn.close()
        return False  # Trả về False nếu username không tồn tại

    # Cập nhật mật khẩu
    cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (hashed_password, username))
    conn.commit()
    conn.close()
    return True  # Trả về True nếu cập nhật thành công

def delete_user(username):
    """Xóa tài khoản khỏi database theo username"""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()


def track_activity(username, action):
    """Ghi nhận hoạt động của người dùng"""
    conn = connect_db()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if action == "login":
        session_id = str(uuid.uuid4())  # Tạo session ID mới
        st.session_state["session_id"] = session_id  # Lưu vào session
    else:
        session_id = st.session_state.get("session_id", None)

    # Ghi nhận hoạt động
    cursor.execute("""
        INSERT INTO user_activity_tracking (username, action, timestamp, session_id)
        VALUES (?, ?, ?, ?)
    """, (username, action, timestamp, session_id))
    conn.commit()
    conn.close()

def get_user_login_info():
    """Lấy thông tin đăng nhập, số lần đăng nhập và tổng thời gian hoạt động"""
    conn = connect_db()
    cursor = conn.cursor()

    query = """
        WITH login_times AS (
            SELECT u.username, u.user_code, u.name, l.session_id, l.timestamp AS login_time
            FROM user_activity_tracking l
            JOIN users u ON l.username = u.username
            WHERE l.action = 'login'
        ),
        logout_times AS (
            SELECT u.username, l.session_id, l.timestamp AS logout_time
            FROM user_activity_tracking l
            JOIN users u ON l.username = u.username
            WHERE l.action = 'logout'
        )
        SELECT 
            l.username,
            l.user_code,
            l.name,
            COUNT(DISTINCT l.session_id) AS total_logins,
            ROUND(SUM(
                CASE 
                    WHEN o.logout_time IS NOT NULL THEN 
                        (julianday(o.logout_time) - julianday(l.login_time)) * 60
                    ELSE 
                        MAX(1, (julianday('now') - julianday(l.login_time)) * 60)
                END
            ), 2) AS total_login_minutes
        FROM login_times l
        LEFT JOIN logout_times o 
        ON l.username = o.username AND l.session_id = o.session_id
        GROUP BY l.username, l.user_code, l.name;
    """
    
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()

    return data


def log_user_activity(user_id, action):
    """Ghi log hoạt động của người dùng vào database"""
    conn = connect_db()
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Nếu là đăng nhập, tạo session_id mới
    if action == "login":
        session_id = str(uuid.uuid4())  # Tạo session ID ngẫu nhiên
    else:
        # Lấy session_id gần nhất của user_id
        cursor.execute("""
            SELECT session_id FROM user_activity_tracking 
            WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1
        """, (user_id,))
        session = cursor.fetchone()
        session_id = session[0] if session else str(uuid.uuid4())  # Nếu chưa có session, tạo mới

    cursor.execute("""
        INSERT INTO user_activity_tracking (user_id, action, timestamp, session_id)
        VALUES (?, ?, ?, ?)
    """, (user_id, action, timestamp, session_id))

    conn.commit()
    conn.close()

def check_username_exists(username):
    """Kiểm tra xem tên tài khoản đã tồn tại trong database hay chưa"""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
    count = cursor.fetchone()[0]
    
    conn.close()
    return count > 0  # Nếu số lượng > 0, tức là username đã tồn tại
