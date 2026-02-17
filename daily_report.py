import os
import sqlite3
from datetime import datetime
from twilio.rest import Client

# Match the DB path used in database.py
DB_PATH = "applications.db"

def send_daily_report():
    """Sends a WhatsApp summary of today's matched jobs to Gopi."""

    # 1. Check database exists
    if not os.path.exists(DB_PATH):
        print("No database found yet. No report to send.")
        return

    # 2. Query today's applications
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        cursor.execute(
            "SELECT job_title, status, link FROM applications WHERE applied_at LIKE ?",
            (f"{today}%",)
        )
        rows = cursor.fetchall()
    except Exception as e:
        print(f"❌ DB query failed: {e}")
        conn.close()
        return
    finally:
        conn.close()

    count = len(rows)

    # 3. Build the WhatsApp message
    if count == 0:
        report_msg = (
            f"📋 *AeroApplied AI Daily Report* ({today})\n\n"
            f"🔍 Search complete — no new matching jobs found today.\n"
            f"🚀 Bot is running on Render Cloud. Try again tomorrow!"
        )
    else:
        job_lines = "\n".join(
            [f"  • {row[0]}\n    🔗 {row[2]}" for row in rows[:10]]
        )
        report_msg = (
            f"📋 *AeroApplied AI Daily Report* ({today})\n\n"
            f"✅ *{count} Matching Jobs Found!*\n\n"
            f"{job_lines}\n\n"
            f"🎯 Roles: Data Scientist / Analyst / ML\n"
            f"👆 Tap a link to Easy Apply now!"
        )

    # 4. Send via Twilio WhatsApp
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token  = os.environ.get("TWILIO_AUTH_TOKEN")
    from_number = os.environ.get("TWILIO_WHATSAPP_NUMBER")  # e.g. whatsapp:+14155238886
    to_number   = os.environ.get("MY_PHONE_NUMBER")          # e.g. whatsapp:+919XXXXXXXXX

    if not all([account_sid, auth_token, from_number, to_number]):
        print("❌ Twilio env vars not set. Cannot send WhatsApp report.")
        print(f"📋 Report would have been:\n{report_msg}")
        return

    try:
        twilio_client = Client(account_sid, auth_token)
        twilio_client.messages.create(
            body=report_msg,
            from_=from_number,
            to=to_number
        )
        print(f"✅ Daily report sent to WhatsApp. ({count} jobs)")
    except Exception as e:
        print(f"❌ Failed to send WhatsApp report: {e}")


if __name__ == "__main__":
    send_daily_report()