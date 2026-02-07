import mysql.connector
import secrets

def initialize_database():
    print("🔌 Connecting to MySQL Server...")
    try:
        # 1. Connect to Server (No DB yet)
        conn = mysql.connector.connect(
            host=secrets.DB_HOST,
            user=secrets.DB_USER,
            password=secrets.DB_PASS
        )
        cursor = conn.cursor()

        # 2. Create the Brain Database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {secrets.DB_NAME}")
        print(f"✅ Database '{secrets.DB_NAME}' checked/created.")

        # 3. Connect to the new Brain
        conn.database = secrets.DB_NAME

        # 4. Create Tables (Memory Structure)
        # Table for User Profile (Name, Preferences)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            id INT AUTO_INCREMENT PRIMARY KEY,
            setting_key VARCHAR(50) UNIQUE,
            setting_value TEXT
        )
        """)
        
        # Table for Chat History (Long Term Memory)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_text TEXT,
            ai_response TEXT
        )
        """)

        print("✅ Memory Tables constructed.")
        conn.close()
        print("🚀 MySQL Setup Complete! Your database is ready.")

    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        print("Tip: Check if your MySQL Server is running in Services.")

if __name__ == "__main__":
    initialize_database()