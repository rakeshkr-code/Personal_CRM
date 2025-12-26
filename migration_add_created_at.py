# migration_add_created_at.py
import sqlite3

conn = sqlite3.connect('personal_crm.db')
cursor = conn.cursor()

# Add created_at column to relationships table
try:
    cursor.execute('''
        ALTER TABLE relationships 
        ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    ''')
    conn.commit()
    print("✓ Added created_at column to relationships table")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("✓ Column already exists")
    else:
        print(f"✗ Error: {e}")

conn.close()
