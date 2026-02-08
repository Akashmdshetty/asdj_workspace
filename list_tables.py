import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), 'db.sqlite3')
print(f"Checking DB at: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables found:")
for t in tables:
    print(f"- {t[0]}")

conn.close()
