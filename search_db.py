import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outreach.db")

if not os.path.exists(db_path):
    print("Could not find outreach.db in this folder! Make sure to place this script in the same directory.")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    found = False
    print("Scanning your outreach database for matching keys...\n" + "="*50)
    
    for table in tables:
        try:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            for row in rows:
                for cell in row:
                    if cell and isinstance(cell, str) and "agy-" in cell:
                        print(f"[FOUND] Table: {table} -> Match: {cell}")
                        found = True
        except Exception as e:
            continue
            
    if not found:
        print("No string starting with 'agy-' was found inside outreach.db.")
    print("="*50)
    conn.close()
