import sqlite3

conn = sqlite3.connect("requests.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_input TEXT,
        intent TEXT,
        status TEXT
    )
""")
conn.commit()

def log_request(user_input, intent, status):
    cursor.execute("INSERT INTO logs (user_input, intent, status) VALUES (?, ?, ?)",
                   (user_input, intent, status))
    conn.commit()
