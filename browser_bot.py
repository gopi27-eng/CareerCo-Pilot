import os
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def start_stealth_browser():
    """Optimized for Render Cloud using Headless Chrome."""
    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # Anti-detection for Headless mode
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    try:
        # Render's environment will provide the binary
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        print(f"❌ Cloud Launch Error: {e}")
        return None

def login_to_linkedin(driver):
    """Logs into LinkedIn using credentials from Render Environment Variables."""
    email = os.environ.get("LINKEDIN_EMAIL")
    password = os.environ.get("LINKEDIN_PASSWORD")
    
    driver.get("https://www.linkedin.com/login")
    time.sleep(random.uniform(2, 4))
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        print("🔐 Logged into LinkedIn successfully.")
        time.sleep(5)
    except Exception as e:
        print(f"❌ Login failed: {e}")

def handle_linkedin_popup(driver):
    """Processes 'Easy Apply' while keeping you logged in."""
    target_words = ["Next", "Review", "Submit application", "Submit"]
    applied_successfully = False

    for i in range(15):
        found = False
        time.sleep(random.uniform(2, 4))
        for word in target_words:
            try:
                xpath = f"//button[contains(., '{word}')] | //button[contains(span, '{word}')]"
                btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                if word in ["Submit application", "Submit"]:
                    applied_successfully = True
                driver.execute_script("arguments[0].scrollIntoView();", btn)
                btn.click()
                found = True
                break
            except:
                continue
        if not found: break
    return applied_successfully