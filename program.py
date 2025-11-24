import time
import requests
import json
import os
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# SETTINGS
TARGET_URL = "ENTER_YOUR_SCHOOL_SYSTEM_URL_HERE"
USERNAME = "ENTER_YOUR_SCHOOL_EMAIL"
PASSWORD = "ENTER_YOUR_PASSWORD"

# Telegram 
TELEGRAM_TOKEN = "ENTER_YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "ENTER_YOUR_CHAT_ID" # You can get your ID using @userinfobot
DB_FILE = "grades.json"

def send_telegram_message(message):
    """Sends a message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
        print(f"📩 Message sent successfully.")
    except Exception as e:
        print(f"Error sending message: {e}")

def load_saved_grades():
    """Loads previously saved grades from the JSON file."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {} 
    return {}

def save_grades(grades):
    """Saves the new grades to the JSON file."""
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(grades, f, ensure_ascii=False, indent=4)
        print(f"💾 Data saved to '{DB_FILE}'.")
    except Exception as e:
        print(f"Error saving file: {e}")

def fetch_grades():
    """Logs into the system, scrapes the grades, and returns them as a dictionary."""
    options = webdriver.ChromeOptions()
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    current_grades = {} 

    try:
        print("🌍 Connecting to the website...")
        driver.get(TARGET_URL)
        time.sleep(3)

        # --- LOGIN AND NAVIGATION STEPS ---
        # Note: These XPaths/IDs are specific to the OIS system. 
        # Update them according to your target website's structure.
        
        # 1. Click initial login selection
        driver.find_element(By.XPATH, "/html/body/div/a[1]/div").click()
        time.sleep(4)

        # 2. Enter Username (Microsoft Login usually)
        driver.find_element(By.ID, "i0116").clear()
        driver.find_element(By.ID, "i0116").send_keys(USERNAME)
        driver.find_element(By.ID, "idSIButton9").click()
        time.sleep(3) 

        # 3. Enter Password
        driver.find_element(By.ID, "i0118").send_keys(PASSWORD)
        driver.find_element(By.ID, "idSIButton9").click()
        time.sleep(3) 

        # 4. Handle 'Stay Signed In?' prompt
        try:
            if "idSIButton9" in driver.page_source:
                driver.find_element(By.ID, "idSIButton9").click()
                time.sleep(3)
        except: pass

        # 5. Navigate through internal portal buttons
        driver.find_element(By.XPATH, "/html/body/div[3]/input").click()
        time.sleep(6) 

        # 6. Navigate to Grades Page via Sidebar
        try:
            driver.find_element(By.ID, "left-menu7").click()
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="sidr-left7"]/a[6]').click()
            time.sleep(5)
        except Exception as e:
            print(f"Menu navigation error: {e}")
            return None
        
        # --- DATA SCRAPING ---
        print("🔍 Scanning the grade table...")
        rows = driver.find_elements(By.TAG_NAME, "tr")
        
        active_course_name = ""
        active_grade = "Not Entered"
        
        course_pattern = re.compile(r"([A-Z0-9İĞÜŞÖÇ\-]+)\s-\s(.+)") 
        
        grade_pattern = re.compile(r"(\d{1,3}\.\d{2})")

        for row in rows:
            text = row.text.strip()
            course_match = course_pattern.search(text)
            
            if course_match and "Ders" not in text:
                if active_course_name != "":
                    current_grades[active_course_name] = active_grade
                
                active_course_name = course_match.group(2) 
                active_grade = "Not Entered"
            
            elif ("Vize" in text or "Ara Sınav" in text or "Final" in text):
                grade_match = grade_pattern.search(text)
                if grade_match:
                    active_grade = grade_match.group(1)

        if active_course_name != "":
            current_grades[active_course_name] = active_grade
            
    except Exception as e:
        print(f"❌ Scraping error: {e}")
        return None 
    finally:
        driver.quit()
    
    return current_grades

def main():
    print("🚀 System Started! Checking every 30 minutes.")
    
    if not os.path.exists(DB_FILE):
        print(f"📂 First setup: '{DB_FILE}' will be created. No notifications for this run.")
    
    while True:
        try:
            now = datetime.now().strftime("%H:%M")
            print(f"\n⏰ Check Time: {now}")

            old_data = load_saved_grades()
            
            new_data = fetch_grades()
            
            if new_data:
                if not old_data:
                    print("💽 First run data saved to database (Silent Mode)...")
                    save_grades(new_data)
                
                else:
                    message_list = []
                    has_changes = False

                    for course, grade in new_data.items():
                        old_grade = old_data.get(course, "Not Entered")
                        
                        if old_grade != grade:
                            has_changes = True
                            
                            if old_grade == "Not Entered" and grade != "Not Entered":
                                message_list.append(f"🔔 *ANNOUNCED!*\n📚 {course}\n📝 Grade: {grade}")
                            elif old_grade != "Not Entered":
                                message_list.append(f"⚠️ *UPDATED!*\n📚 {course}\nOld: {old_grade} -> New: {grade}")

                    if message_list:
                        final_message = "\n\n".join(message_list)
                        send_telegram_message(final_message)
                        save_grades(new_data)
                        print("✅ Notifications sent and database updated.")
                    elif has_changes:
                         save_grades(new_data)
                         print("💾 Database updated silently.")
                    else:
                        print("💤 No changes detected.")
            
            else:
                print("⚠️ Could not fetch data, skipping this turn.")

        except Exception as e:
            print(f"General Loop Error: {e}")

        print("⏳ Waiting 30 minutes...")
        time.sleep(1800) 

if __name__ == "__main__":
    main()