import sqlite3
import hashlib

# Hàm hash mật khẩu
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Hàm kiểm tra và tạo admin mặc định
def create_default_admin():
    conn = sqlite3.connect("data/data.db")
    cursor = conn.cursor()
    
    # Kiểm tra xem admin có tồn tại chưa
    cursor.execute("SELECT * FROM users WHERE username = ?", ("Admin1",))
    admin = cursor.fetchone()
    
    if not admin:
        password_hash = hash_password("tung123123")
        cursor.execute("""
            INSERT INTO users (username, password_hash, role, user_code, name, email, major)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("Admin1", password_hash, "admin", "A0001", "Admin", "admin@example.com", "N/A"))
        conn.commit()
        print("✅ Tài khoản admin mặc định đã được tạo!")
    else:
        print("⚡ Admin đã tồn tại.")

    conn.close()

# Chạy khi khởi động
if __name__ == "__main__":
    create_default_admin()
