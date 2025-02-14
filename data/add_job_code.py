import sqlite3

def update_jobs_table():
    conn = sqlite3.connect("data/data.db")
    cursor = conn.cursor()
    
    # Thêm cột job_code nếu chưa có
    cursor.execute("PRAGMA table_info(jobs)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "job_code" not in columns:
        cursor.execute("ALTER TABLE jobs ADD COLUMN job_code TEXT")
        conn.commit()

    conn.close()

update_jobs_table()
