import sqlite3

def create_database():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    
    # Bảng Người Dùng
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT CHECK(role IN ('student', 'lecturer', 'admin')) NOT NULL,
        user_code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        major TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_verified BOOLEAN DEFAULT 0
    )''')
    
    # Bảng Phiên Đăng Nhập
    cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (
        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        token TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )''')
    
    # Bảng Môn Học
    cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL,
        description TEXT
    )''')
    
    # Bảng Người Dùng - Môn Học
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        course_id INTEGER,
        class_time TEXT,
        room TEXT,
        lecturer_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
        FOREIGN KEY (lecturer_id) REFERENCES users(user_id) ON DELETE SET NULL
    )''')
    
    # Bảng Lịch Thi
    cursor.execute('''CREATE TABLE IF NOT EXISTS exam_schedules (
        exam_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER,
        exam_date TEXT NOT NULL,
        exam_time TEXT NOT NULL,
        room TEXT NOT NULL,
        FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
    )''')
    
    # Bảng Thông Tin Hành Chính
    cursor.execute('''CREATE TABLE IF NOT EXISTS admin_info (
        info_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Bảng Tài Liệu Học Tập
    cursor.execute('''CREATE TABLE IF NOT EXISTS resources (
        resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER,
        title TEXT NOT NULL,
        file_url TEXT NOT NULL,
        FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
    )''')
    
    # Bảng Việc Làm
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
        job_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        requirements TEXT NOT NULL,
        salary TEXT,
        job_type TEXT CHECK(job_type IN ('full-time', 'internship')) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Bảng Ứng Tuyển Việc Làm
    cursor.execute('''CREATE TABLE IF NOT EXISTS applications (
        application_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        job_id INTEGER,
        resume_url TEXT NOT NULL,
        cover_letter TEXT NOT NULL,
        status TEXT CHECK(status IN ('pending', 'accepted', 'rejected')) DEFAULT 'pending',
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE
    )''')
    
    # Bảng Bài Đăng Cộng Đồng
    cursor.execute('''CREATE TABLE IF NOT EXISTS forum_posts (
        post_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        topic TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )''')
    
    # Bảng Bình Luận
    cursor.execute('''CREATE TABLE IF NOT EXISTS comments (
        comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER,
        user_id INTEGER,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post_id) REFERENCES forum_posts(post_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )''')
    
    # Bảng Lịch Sử Tìm Kiếm
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_activity (
        activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action_type TEXT CHECK(action_type IN ('search', 'click', 'view', 'chat')) NOT NULL,
        query TEXT,
        response TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )''')
    
    conn.commit()
    conn.close()
    print("Database created successfully and saved as data.db")

if __name__ == "__main__":
    create_database()
