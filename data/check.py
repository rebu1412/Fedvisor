import sqlite3

# Kết nối đến cơ sở dữ liệu SQLite
db_path = 'data/data.db'  # Thay đổi đường dẫn nếu cần
conn = sqlite3.connect(db_path)

# Tạo con trỏ để thực thi câu lệnh SQL
cursor = conn.cursor()

# Câu lệnh SQL để lấy tên các bảng
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Lấy tất cả các bảng trong cơ sở dữ liệu
tables = cursor.fetchall()

# Kiểm tra và hiển thị các bảng và cột của mỗi bảng
if tables:
    for table in tables:
        table_name = table[0]
        print(f"Bảng: {table_name}")
        
        # Lấy thông tin các cột trong bảng
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        # Hiển thị các cột
        if columns:
            print("Cột trong bảng:")
            for column in columns:
                print(f"- {column[1]} (Loại dữ liệu: {column[2]})")  # column[1] là tên cột, column[2] là kiểu dữ liệu
        else:
            print("Không có cột nào.")
        print("-" * 40)  # Tạo đường kẻ phân cách giữa các bảng
else:
    print("Không có bảng nào trong cơ sở dữ liệu.")

# Đóng kết nối
conn.close()