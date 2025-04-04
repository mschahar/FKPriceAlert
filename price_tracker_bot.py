import os
import time
import re
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Bot
from telegram.error import TelegramError

# Flipkart product URLs to track
PRODUCT_URLS = [
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1-1200-mm-3-blade-ceiling-fan/p/itmfaf147854846b",
    "https://www.flipkart.com/orient-electric-ujala-air-1-star-1200-mm-3-blade-ceiling-fan/p/itm86c3958e8a4e0",
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1200-mm-3-blade-ceiling-fan/p/itme0dfe1a5d5737"
]

# Set your Telegram bot token and chat ID
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def get_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(
        ChromeDriverManager().install(),
        options=chrome_options
    )

def get_price_from_flipkart(browser, url):
    browser.get(url)
    time.sleep(5)  # Let JS load fully
    
    print(f"🟡 Page title: {browser.title}")

    # Try multiple known selectors
    selectors = ["._30jeq3", "._16Jk6d", "div[class*='price']"]
    for selector in selectors:
        try:
            price_element = browser.find_element(By.CSS_SELECTOR, selector)
            price_text = price_element.text.strip()
            if "₹" in price_text:
                return price_text
        except:
            continue

    # Fallback: regex scan for ₹xxxx in the full page source
    print("⚠️ Falling back to regex scan")
    page_source = browser.page_source
    match = re.search(r'₹\s?[\d,]+', page_source)
    if match:
        return match.group().strip()

    raise Exception("Could not extract price: No valid selector or price pattern found.")

async def send_telegram_message(text):
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
    except TelegramError as e:
        print(f"⚠️ Telegram send error: {e}")

def check_price():
    browser = get_browser()
    for url in PRODUCT_URLS:
        print(f"Checking: {url}")
        try:
            price = get_price_from_flipkart(browser, url)
            msg = f"✅ Price for:\n{url}\nis {price}"
            print(msg)
            asyncio.run(send_telegram_message(msg))
        except Exception as e:
            print(f"❌ Could not get price from {url}\nReason: {e}")
    browser.quit()

if __name__ == "__main__":
    check_price()
