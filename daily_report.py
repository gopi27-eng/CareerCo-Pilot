import sqlite3
import os
from twilio.rest import Client
from datetime import datetime

def send_daily_report():
    # 1. Connect to the database
    # In Render, this file stays in the root directory
    db_path = 'job_automation.db'
    
    if not os.path.exists(db_path):
        print("No database found yet. No report to send.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 2. Get today's stats
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT COUNT(*) FROM applications WHERE date LIKE ?", (f"{today}%",))
    count = cursor.fetchone()[0]

    # 3. Format the message for Gopi
    report_msg = (
        f"📋 *AeroApplied AI Daily Report* ({today})\n\n"
        f"✅ Total Applications Today: {count}\n"
        f"🎯 Targeted Roles: Data Scientist / Analyst\n"
        f"🚀 Status: System Running on Render Cloud"
    )

    # 4. Send via Twilio
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_whatsapp = os.environ.get('TWILIO_WHATSAPP_NUMBER') # e.g., 'whatsapp:+14155238886'
    to_whatsapp = os.environ.get('MY_PHONE_NUMBER') # Your WhatsApp number

    client = Client(account_sid, auth_token)
    
    try:
        client.messages.create(
            body=report_msg,
            from_=from_whatsapp,
            to=to_whatsapp
        )
        print("✅ Daily report sent to WhatsApp.")
    except Exception as e:
        print(f"❌ Failed to send report: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    send_daily_report()