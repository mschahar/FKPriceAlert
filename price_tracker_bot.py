import time
import re
import telegram
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

# === Hardcoded Telegram Bot Credentials ===
TOKEN = "7866528662:AAHjd1BAefRm0RBYvy_KPql23HqMAx__VNI"
CHAT_ID = "163447880"

# Initialize bot
bot = telegram.Bot(token=TOKEN)

# Product URLs to monitor
product_urls = [
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1-1200-mm-3-blade-ceiling-fan/p/itmfaf147854846b",
    "https://www.flipkart.com/orient-electric-ujala-air-1-star-1200-mm-3-blade-ceiling-fan/p/itm86c3958e8a4e0",
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1200-mm-3-blade-ceiling-fan/p/itme0dfe1a5d5737"
]

# Send Telegram message
def send_telegram_message(message):
    try:
        if TOKEN and CHAT_ID:
            bot.send_message(chat_id=CHAT_ID, text=message)
        else:
            print("⚠️ Telegram send error: Chat_id or token is not set")
    except Exception as e:
        print(f"⚠️ Telegram send error: {e}")

# Setup headless browser
def get_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

# Fallback regex price extraction
def extract_price_from_page_source(page_source):
    match = re.search(r'₹\s?[0-9,]+', page_source)
    if match:
        return match.group()
    return None

# Main logic
def check_price():
    browser = get_browser()
    for url in product_urls:
        print(f"Checking: {url}")
        try:
            browser.get(url)
            time.sleep(2)
            print("🟡 Page title:", browser.title)

            try:
                # First try via Selenium selector
                price_elem = browser.find_element("css selector", "._30jeq3")
                price = price_elem.text
            except NoSuchElementException:
                # Fallback to regex scan
                print("⚠️ Falling back to regex scan")
                price = extract_price_from_page_source(browser.page_source)

            if price:
                print(f"✅ Price for:\n{url}\nis {price}")
                send_telegram_message(f"🛒 Price for:\n{url}\nis {price}")
            else:
                print(f"❌ Could not extract price for {url}")
        except Exception as e:
            print(f"❌ Could not get price from {url}\nReason: {e}")
    browser.quit()

# Entry point
if __name__ == "__main__":
    check_price()
