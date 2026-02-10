import time
import os
from browser_bot import start_stealth_browser, handle_linkedin_popup, login_to_linkedin
from matcher import is_good_match
from database import log_application
from daily_report import send_daily_report

def run_automation():
    """
    Orchestrates the job search and application process on Render Cloud.
    Targeting Data Science roles for Gopi Borra (9.00 SGPA).
    """
    print("🎬 Starting AeroApplied AI Automation...")
    driver = start_stealth_browser()
    
    if not driver:
        print("❌ Failed to initialize headless browser.")
        return

    try:
        # 1. Login to LinkedIn using Render Env Vars
        login_to_linkedin(driver)
        
        # 2. Search for Data Science Roles in India with Easy Apply
        # f_AL=true filters for 'Easy Apply' jobs
        search_url = "https://www.linkedin.com/jobs/search/?keywords=Data%20Scientist&location=India&f_AL=true"
        driver.get(search_url)
        time.sleep(5)

        # 3. Locate Job Cards
        # Note: Selectors may need adjustment based on LinkedIn's dynamic HTML
        job_cards = driver.find_elements("class name", "job-card-container")[:10] 
        print(f"🔍 Found {len(job_cards)} potential job matches.")

        for index, card in enumerate(job_cards):
            try:
                # Scroll and Click the job card
                driver.execute_script("arguments[0].scrollIntoView();", card)
                card.click()
                time.sleep(3)
                
                # Extract description to check match with M.Sc Data Science skills
                job_details_element = driver.find_element("id", "job-details")
                job_text = job_details_element.text
                
                if is_good_match(job_text):
                    print(f"🎯 Match found for Job {index+1}! Proceeding with Easy Apply...")
                    
                    # 4. Handle the multi-step popup
                    success = handle_linkedin_popup(driver)
                    
                    if success:
                        # Log to SQLite (persistence on Render)
                        log_application("LinkedIn", "Data Scientist", "Applied")
                        print(f"✅ Application {index+1} submitted successfully.")
                else:
                    print(f"⏩ Job {index+1} did not meet technical criteria. Skipping.")

            except Exception as e:
                print(f"⚠️ Error processing job {index+1}: {e}")
                continue

        # 5. Final Step: Send the Daily Report to Gopi's WhatsApp
        print("📊 Generating daily summary report...")
        send_daily_report()

    except Exception as e:
        print(f"❌ Critical Automation Error: {e}")
    finally:
        # Close the headless session
        driver.quit()
        print("🏁 Automation cycle complete. Browser closed.")

if __name__ == "__main__":
    # For local testing; in production, this is triggered by whatsapp_server.py
    run_automation()