import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import asyncio
from telegram import Bot

# --- Configuration ---
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
TARGET_PRICE = 1099

PRODUCT_URLS = [
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1-1200-mm-3-blade-ceiling-fan/p/itmfaf147854846b",
    "https://www.flipkart.com/orient-electric-ujala-air-1-star-1200-mm-3-blade-ceiling-fan/p/itm86c3958e8a4e0",
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1200-mm-3-blade-ceiling-fan/p/itme0dfe1a5d5737"
]

# --- Set up Selenium browser ---
def get_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920x1080")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# --- Get price from a Flipkart product page ---
def get_price(browser, url):
    browser.get(url)
    time.sleep(3)  # Give it time to load

    try:
        price_element = browser.find_element(By.CSS_SELECTOR, "._30jeq3")
        price_text = price_element.text.strip().replace("₹", "").replace(",", "")
        return int(price_text)
    except Exception as e:
        raise Exception(f"Could not extract price: {str(e)}")

# --- Send Telegram message ---
async def send_telegram_alert(bot, message):
    await bot.send_message(chat_id=CHAT_ID, text=message)

# --- Main logic ---
def check_price():
    browser = get_browser()
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    for url in PRODUCT_URLS:
        print(f"Checking: {url}")
        try:
            price = get_price(browser, url)
            print(f"✅ Price found: ₹{price}")
            if price <= TARGET_PRICE:
                message = f"✅ Price Drop Alert!\n{url}\nCurrent Price: ₹{price}"
                asyncio.run(send_telegram_alert(bot, message))
        except Exception as e:
            print(f"❌ Could not get price from {url}\nReason: {e}")
            asyncio.run(send_telegram_alert(bot, f"⚠️ Couldn't fetch price for:\n{url}"))

    browser.quit()

# --- Run the script ---
if __name__ == "__main__":
    check_price()
