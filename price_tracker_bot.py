import asyncio
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Bot

# 🔧 Telegram Bot Details
TOKEN = "7866528662:AAFZhfnmx613vezBMjcbpYKzvvpQHhdMYAw"
CHAT_ID = "163447880"
bot = Bot(token=TOKEN)

# 🔗 Product URLs and their target prices
product_urls = [
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1-1200-mm-3-blade-ceiling-fan/p/itmfaf147854846b",
    "https://www.flipkart.com/orient-electric-ujala-air-1-star-1200-mm-3-blade-ceiling-fan/p/itm86c3958e8a4e0",
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1200-mm-3-blade-ceiling-fan/p/itme0dfe1a5d5737"
]

target_prices = {
    product_urls[0]: 1100,
    product_urls[1]: 1100,
    product_urls[2]: 1100
}

# 📤 Send Telegram message
async def send_telegram_message(product_url, price):
    try:
        message = (
            "⚠️〽️ *Price Drop Alert!*\n\n"
            "🔥💰 A tracked product just changed price!\n\n"
            f"🛒⏩ [View Product]({product_url})\n"
            f"💸🤑 *New Price:* ₹{price}\n\n"
            "✅🛍️ Buy fast!"
        )
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
    except Exception as e:
        print(f"⚠️ Telegram send error: {e}")

# 🚀 Headless browser setup
def get_browser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 🔢 Parse ₹1,399 → 1399
def parse_price(price_str):
    return int(re.sub(r"[^\d]", "", price_str))

# 🧪 Main price checker
async def check_price():
    browser = get_browser()
    wait = WebDriverWait(browser, 15)

    for url in product_urls:
        print(f"\n🔍 Checking: {url}")
        try:
            browser.get(url)
            price_elem = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="_30jeq3" and not(ancestor::div[contains(@class, "_3I9_wc")])]')
                )
            )
            price_str = price_elem.text
            price_int = parse_price(price_str)
            print(f"💰 Price for:\n{url}\n→ ₹{price_int}")

            # Filter out junk prices like ₹132 or ₹108
            if price_int < 500:
                print(f"❌ Ignoring junk price ₹{price_int}")
                continue

            if price_int <= target_prices[url]:
                await send_telegram_message(url, price_int)
            else:
                print(f"ℹ️ ₹{price_int} is above your target of ₹{target_prices[url]} — no alert.")
        except TimeoutException:
            print("⚠️ Price element not found.")
        except Exception as e:
            print(f"❌ Error checking {url}:\n{e}")

    browser.quit()

# ▶️ Run the script
if __name__ == "__main__":
    asyncio.run(check_price())
