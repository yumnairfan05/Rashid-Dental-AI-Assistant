import sqlite3

DATABASE = "appointments.db"

def get_connection():
    return sqlite3.connect(DATABASE)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            preferred_date TEXT,
            message TEXT
        )
    """)

    conn.commit()
    conn.close()