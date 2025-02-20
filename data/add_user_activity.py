import sqlite3

DB_PATH = "data/data.db"
def connect_db():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def create_user_activity():
    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_activity (
            activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action_type TEXT,
            query TEXT,
            response TEXT,
            timestamp TIMESTAP DEFAULT CURRENT_TIMESTAMP               
        )
    """)
    conn.commit()

create_user_activity()
print("Chạy thành công!")