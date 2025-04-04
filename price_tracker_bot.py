import os
import time
import telegram
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Telegram config from GitHub Secrets or environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Set your target price
TARGET_PRICE = 1099

# Flipkart product URLs to track
PRODUCT_URLS = [
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1-1200-mm-3-blade-ceiling-fan/p/itmfaf147854846b",
    "https://www.flipkart.com/orient-electric-ujala-air-1-star-1200-mm-3-blade-ceiling-fan/p/itm86c3958e8a4e0",
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1200-mm-3-blade-ceiling-fan/p/itme0dfe1a5d5737"
]

# Setup Selenium Chrome browser
def get_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 Chrome/123.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=chrome_options)
    return browser

# Get price from product page
def get_price_from_page(browser, url):
    browser.get(url)
    time.sleep(4)
    try:
        price_element = browser.find_element(By.CLASS_NAME, "_30jeq3")
        price_text = price_element.text.strip().replace("₹", "").replace(",", "")
        return int(price_text)
    except Exception as e:
        print(f"❌ Could not get price from {url}")
        print(f"Reason: {e}")
        return None

# Main logic
def check_price():
    browser = get_browser()
    for url in PRODUCT_URLS:
        print(f"Checking: {url}")
        try:
            price = get_price_from_page(browser, url)
            if price is None:
                bot.send_message(chat_id=CHAT_ID, text=f"⚠️ Couldn't fetch price for:\n{url}")
            elif price <= TARGET_PRICE:
                message = f"✅ Price Alert!\n₹{price} is below ₹{TARGET_PRICE} 🎯\n{url}"
                bot.send_message(chat_id=CHAT_ID, text=message)
            else:
                print(f"Price is ₹{price}, above target ₹{TARGET_PRICE}")
        except Exception as e:
            print(f"Error while checking:\n{url}\nError: {e}")
            bot.send_message(chat_id=CHAT_ID, text=f"🔴 Error while checking:\n{url}\nError: {e}")
    browser.quit()

# Run script
if __name__ == "__main__":
    check_price()
