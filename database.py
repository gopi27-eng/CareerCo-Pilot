import sqlite3
from datetime import datetime

def log_application(platform, role, status):
    conn = sqlite3.connect('job_automation.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications 
        (id INTEGER PRIMARY KEY, date TEXT, platform TEXT, role TEXT, status TEXT)
    ''')
    cursor.execute("INSERT INTO applications (date, platform, role, status) VALUES (?, ?, ?, ?)",
                   (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), platform, role, status))
    conn.commit()
    conn.close()