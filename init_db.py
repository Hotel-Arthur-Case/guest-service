# database.py
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('hotel_guests.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            preferences TEXT,
            allergy TEXT,
            loyalty_points INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Initialize the database when running this file directly
    init_db()
    print("Database initialized.")
