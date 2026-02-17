import sqlite3
import os
from datetime import datetime

DB_PATH = "applications.db"

def init_db():
    """Creates the applications table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            platform  TEXT,
            job_title TEXT,
            status    TEXT,
            link      TEXT,
            applied_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_application(platform, job_title, status, link=""):
    """Logs a job application to the SQLite database."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Avoid duplicates — check if this job title was already logged today
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        "SELECT id FROM applications WHERE job_title = ? AND applied_at LIKE ?",
        (job_title, f"{today}%"),
    )
    if cursor.fetchone():
        print(f"  ⏭️ Already logged today: {job_title}")
        conn.close()
        return

    cursor.execute(
        "INSERT INTO applications (platform, job_title, status, link, applied_at) VALUES (?, ?, ?, ?, ?)",
        (platform, job_title, status, link, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()
    print(f"  💾 Logged: {job_title} [{status}]")

def get_todays_applications():
    """Returns all applications logged today."""
    if not os.path.exists(DB_PATH):
        return []
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        "SELECT platform, job_title, status, link, applied_at FROM applications WHERE applied_at LIKE ?",
        (f"{today}%",),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows