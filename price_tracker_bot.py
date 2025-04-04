import time
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Bot

# Telegram bot details
API_TOKEN = "7866528662:AAHjd1BAefRm0RBYvy_KPql23HqMAx__VNI"
CHAT_ID = "163447880"
bot = Bot(token=API_TOKEN)

# Flipkart product URLs (all Orient 1200mm fans)
PRODUCT_URLS = [
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1-1200-mm-3-blade-ceiling-fan/p/itmfaf147854846b",
    "https://www.flipkart.com/orient-electric-ujala-air-1-star-1200-mm-3-blade-ceiling-fan/p/itm86c3958e8a4e0",
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1200-mm-3-blade-ceiling-fan/p/itme0dfe1a5d5737"
]

def get_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_price_from_flipkart(browser, url):
    browser.get(url)
    time.sleep(3)  # wait for page to load
    try:
        price_element = browser.find_element(By.CSS_SELECTOR, "._30jeq3")
        return price_element.text.strip()
    except Exception as e:
        raise Exception(f"Could not extract price: {e}")

async def send_telegram_alert(bot, message):
    await bot.send_message(chat_id=CHAT_ID, text=message)

def check_price():
    browser = get_browser()

    for url in PRODUCT_URLS:
        print(f"Checking: {url}")
        try:
            price = get_price_from_flipkart(browser, url)
            message = f"✅ Price fetched for:\n{url}\n💰 Price: {price}"
            print(message)
        except Exception as e:
            message = f"❌ Could not get price from {url}\nReason: {e}"
            print(message)
        try:
            asyncio.run(send_telegram_alert(bot, message))
        except Exception as e:
            print(f"⚠️ Telegram send error: {e}")

    browser.quit()

if __name__ == "__main__":
    check_price()
