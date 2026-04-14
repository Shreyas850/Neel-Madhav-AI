import mysql.connector
import app_secrets as secrets

try:
    mydb = mysql.connector.connect(
      host=secrets.DB_HOST,
      user=secrets.DB_USER,
      password=secrets.DB_PASS
    )

    mycursor = mydb.cursor()
    mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {secrets.DB_NAME}")
    print(f"✅ Success! Database '{secrets.DB_NAME}' is ready for Neel Madhav.")

except Exception as e:
    print(f"❌ Connection Failed. Error: {e}")