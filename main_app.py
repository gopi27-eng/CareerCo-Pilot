import time
import random
from browser_bot import (
    start_stealth_browser,
    login_to_linkedin,
    search_easy_apply_jobs,
    get_job_description,
)
from matcher import is_good_match
from database import log_application
from daily_report import send_daily_report


# ─────────────────────────────────────────────
# Search profiles — broaden to maximise results
# ─────────────────────────────────────────────
SEARCH_QUERIES = [
    ("Data Scientist",       "India"),
    ("Data Analyst",         "India"),
    ("Machine Learning",     "India"),
    ("Python Developer",     "India"),
    ("Business Analyst",     "India"),
    ("AI Engineer",          "India"),
]


def run_automation():
    """
    Orchestrates the job search process on Render Cloud (no Chrome needed).
    Finds matching Easy Apply jobs and sends a WhatsApp daily report.
    """
    print("🎬 Starting AeroApplied AI Automation (Lightweight Mode)...")

    # 1. Start a requests-based session (no Selenium / Chrome)
    session = start_stealth_browser()
    if not session:
        print("❌ Failed to start HTTP session.")
        return

    # 2. Login to LinkedIn
    logged_in = login_to_linkedin(session)
    if not logged_in:
        print("❌ Aborting — could not log into LinkedIn.")
        send_daily_report()   # still send report so you know it ran
        return

    total_found  = 0
    total_logged = 0

    try:
        for keyword, location in SEARCH_QUERIES:
            print(f"\n🔍 Searching: '{keyword}' in {location}")

            jobs = search_easy_apply_jobs(session, keyword, location, max_jobs=5)

            if not jobs:
                print(f"  ⚠️ No jobs returned for '{keyword}'.")
                continue

            for job in jobs:
                total_found += 1
                print(f"\n  🎯 [{total_found}] {job['title']} @ {job['company']}")

                # Fetch job description for matching
                description = get_job_description(session, job["link"])
                time.sleep(random.uniform(1.5, 3.0))   # polite delay

                if description and is_good_match(description):
                    print(f"  ✅ Match! Logging to database...")
                    log_application(
                        platform="LinkedIn",
                        job_title=f"{job['title']} @ {job['company']}",
                        status="Found - Easy Apply",
                        link=job["link"],
                    )
                    total_logged += 1
                else:
                    print(f"  ⏩ Skipping — does not meet criteria.")

            # Polite pause between search queries
            time.sleep(random.uniform(3, 6))

    except Exception as e:
        print(f"❌ Critical Automation Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        print(f"\n📊 Summary — Scanned: {total_found} | Logged: {total_logged}")
        print("📲 Generating daily summary report...")
        send_daily_report()
        print("🏁 Automation cycle complete.")


if __name__ == "__main__":
    run_automation()