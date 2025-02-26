from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuration
BOT_USERNAME = "me"  # Bot's Instagram username
BOT_PASSWORD = "habibi.maryouma"  # Bot's Instagram password
TRIGGER_USER = "mariem.turki_"       # User who can activate the bot
RESPONSE_MESSAGE = "habibi ochrb me" # Message to send every 30 minutes
CHECK_INTERVAL = 1800                  # Check for new messages every 1800 seconds

# Setup Chrome
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)

def login():
    driver.get("https://www.instagram.com/")
    
    # Login
    username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
    
    username_field.send_keys(BOT_USERNAME)
    password_field.send_keys(BOT_PASSWORD)
    password_field.send_keys(Keys.RETURN)
    
    # Dismiss pop-ups
    for popup_text in ["Not Now", "Not Now"]:
        try:
            popup = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[text()='{popup_text}']")))
            popup.click()
        except Exception:
            pass

def check_trigger_message():
    driver.get("https://www.instagram.com/direct/inbox/")
    time.sleep(3)
    
    # Check messages from the trigger user
    try:
        chat = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[text()='{TRIGGER_USER}']/ancestor::a")))
        chat.click()
        time.sleep(2)
        
        # Get the latest message text
        messages = driver.find_elements(By.CSS_SELECTOR, "div._aok span._aok")
        if messages and messages[-1].text.strip().lower() == "activate":
            return True
    except Exception:
        pass
    return False

def send_response():
    message_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//textarea[@placeholder='Message...']")))
    message_box.send_keys(RESPONSE_MESSAGE)
    message_box.send_keys(Keys.RETURN)
    print(f"Sent: {RESPONSE_MESSAGE}")

def main():
    login()
    activated = False
    
    while True:
        if not activated:
            if check_trigger_message():
                activated = True
                print("Bot activated! Starting response loop...")
            else:
                print("Waiting for activation message...")
                time.sleep(CHECK_INTERVAL)
        else:
            send_response()
            time.sleep(30 * 60)  # 30-minute interval

if __name__ == "__main__":
    try:
        main()
    finally:
        driver.quit()
