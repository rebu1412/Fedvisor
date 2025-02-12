import sqlite3

# Kết nối database
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# Truy vấn dữ liệu từ bảng users
cursor.execute("SELECT username, password_hash FROM users;")
accounts = cursor.fetchall()

# Hiển thị danh sách tài khoản & mật khẩu
print("📌 Danh sách tài khoản & mật khẩu:")
for username, password in accounts:
    print(f"👤 {username} | 🔑 {password}")

# Đóng kết nối
conn.close()
