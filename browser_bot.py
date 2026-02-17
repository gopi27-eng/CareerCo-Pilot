import os
import time
import random
import requests
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────
# LinkedIn session via requests (no Chrome needed)
# ─────────────────────────────────────────────

SESSION = None

def start_stealth_browser():
    """
    Returns a requests.Session that mimics a real browser.
    No Chrome / Selenium needed — works on Render free tier (512 MB).
    """
    global SESSION
    session = requests.Session()
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    })
    SESSION = session
    print("✅ Lightweight HTTP session started (no Chrome needed).")
    return session


def login_to_linkedin(session):
    """
    Logs into LinkedIn using form POST — no browser required.
    Returns True on success.
    """
    email = os.environ.get("LINKEDIN_EMAIL")
    password = os.environ.get("LINKEDIN_PASSWORD")

    if not email or not password:
        print("❌ LINKEDIN_EMAIL / LINKEDIN_PASSWORD not set in Render env vars.")
        return False

    try:
        # Step 1 — get CSRF token from login page
        login_page = session.get("https://www.linkedin.com/login", timeout=30)
        soup = BeautifulSoup(login_page.text, "html.parser")
        csrf_tag = soup.find("input", {"name": "loginCsrfParam"})
        csrf = csrf_tag["value"] if csrf_tag else ""

        # Step 2 — submit credentials
        payload = {
            "session_key": email,
            "session_password": password,
            "loginCsrfParam": csrf,
        }
        resp = session.post(
            "https://www.linkedin.com/checkpoint/lg/login-submit",
            data=payload,
            timeout=30,
            allow_redirects=True,
        )

        # Step 3 — verify login by checking for feed redirect
        if "feed" in resp.url or "mynetwork" in resp.url or resp.status_code == 200:
            print("🔐 Logged into LinkedIn successfully.")
            return True
        else:
            print(f"⚠️ Login redirect went to: {resp.url}")
            return False

    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False


def search_easy_apply_jobs(session, keyword="Data Scientist", location="India", max_jobs=10):
    """
    Searches LinkedIn Jobs for Easy Apply listings and returns job data.
    Uses the public-facing JSON endpoint LinkedIn exposes for job cards.
    """
    jobs = []
    start = 0

    try:
        url = (
            "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
            f"?keywords={keyword.replace(' ', '%20')}"
            f"&location={location}"
            f"&f_AL=true"          # Easy Apply only
            f"&start={start}"
        )
        resp = session.get(url, timeout=30)
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.find_all("div", {"class": "base-card"})

        print(f"  📋 Found {len(cards)} cards for '{keyword}'")

        for card in cards[:max_jobs]:
            try:
                title_tag = card.find("h3", {"class": "base-search-card__title"})
                company_tag = card.find("h4", {"class": "base-search-card__subtitle"})
                link_tag = card.find("a", {"class": "base-card__full-link"})
                job_id_tag = card.get("data-entity-urn", "")

                title = title_tag.text.strip() if title_tag else "Unknown"
                company = company_tag.text.strip() if company_tag else "Unknown"
                link = link_tag["href"].split("?")[0] if link_tag else ""
                job_id = job_id_tag.split(":")[-1] if job_id_tag else ""

                if title and link:
                    jobs.append({
                        "title": title,
                        "company": company,
                        "link": link,
                        "job_id": job_id,
                    })
            except Exception as e:
                continue

    except Exception as e:
        print(f"  ⚠️ Search error for '{keyword}': {e}")

    return jobs


def get_job_description(session, job_url):
    """Fetches the full job description text for matching."""
    try:
        resp = session.get(job_url, timeout=30)
        soup = BeautifulSoup(resp.text, "html.parser")
        desc = soup.find("div", {"class": "description__text"})
        return desc.get_text(separator=" ").strip() if desc else ""
    except Exception as e:
        print(f"  ⚠️ Could not fetch job description: {e}")
        return ""


def handle_linkedin_popup(session):
    """
    Easy Apply via the API is not feasible with plain requests alone
    (LinkedIn's apply flow requires JS). This returns False to skip
    auto-applying while still allowing the job to be logged.
    For now, the bot FINDS and LOGS matching jobs, and you apply manually.
    """
    return False