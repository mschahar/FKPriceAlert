import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Bot
from telegram.error import TelegramError

# Replace these with your actual bot token and chat ID
API_TOKEN = "7866528662:AAHjd1BAefRm0RBYvy_KPql23HqMAx__VNI"
CHAT_ID = "163447880"

# Product URLs to track
PRODUCT_URLS = [
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1-1200-mm-3-blade-ceiling-fan/p/itmfaf147854846b",
    "https://www.flipkart.com/orient-electric-ujala-air-1-star-1200-mm-3-blade-ceiling-fan/p/itm86c3958e8a4e0",
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1200-mm-3-blade-ceiling-fan/p/itme0dfe1a5d5737"
]

def get_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

def get_price(browser, url):
    browser.get(url)
    try:
        price_element = browser.find_element(By.CSS_SELECTOR, "._30jeq3")
        return price_element.text.strip()
    except Exception as e:
        raise Exception(f"Could not extract price: {str(e)}")

async def send_telegram_alert(bot, message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except TelegramError as e:
        print(f"Telegram Error: {e}")

def check_price():
    browser = get_browser()
    bot = Bot(token=API_TOKEN)

    for url in PRODUCT_URLS:
        print(f"Checking: {url}")
        try:
            price = get_price(browser, url)
            print(f"✅ Price: {price}")
            asyncio.run(send_telegram_alert(bot, f"🟢 Price of product:\n{url}\n💰 {price}"))
        except Exception as e:
            print(f"❌ Could not get price from {url}\nReason: {e}")
            asyncio.run(send_telegram_alert(bot, f"⚠️ Couldn't fetch price for:\n{url}"))

    browser.quit()

if __name__ == "__main__":
    check_price()
