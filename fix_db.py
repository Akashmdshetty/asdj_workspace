import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), 'db.sqlite3')
print(f"Connecting to {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. Drop table if exists
print("Dropping table core_connectionrequest...")
cursor.execute("DROP TABLE IF EXISTS core_connectionrequest")

# 2. Clear migration history for 0002
print("Removing migration record...")
cursor.execute("DELETE FROM django_migrations WHERE app='core' AND name='0002_user_unique_id_connectionrequest'")

conn.commit()
conn.close()
print("Done.")
