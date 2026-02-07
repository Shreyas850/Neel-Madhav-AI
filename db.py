import sqlite3
import os

DB_FILE = "jarvis_settings.db"

def init_db():
    """Creates the database if it doesn't exist"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    conn.commit()
    conn.close()

def fetch(key):
    """Get a value by key"""
    if not os.path.exists(DB_FILE): init_db()
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else None

def save(key, value):
    """Save or update a value"""
    if not os.path.exists(DB_FILE): init_db()
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

# Initialize on first run
init_db()

# Set default user name if missing
if not fetch("user_name"):
    save("user_name", "Sir")