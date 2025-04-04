import asyncio
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Bot

# 🔧 Telegram Bot Details
TOKEN = "7866528662:AAFZhfnmx613vezBMjcbpYKzvvpQHhdMYAw"
CHAT_ID = "163447880"
bot = Bot(token=TOKEN)

# 🔗 Products and Target Prices
product_urls = [
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1-1200-mm-3-blade-ceiling-fan/p/itmfaf147854846b",
    "https://www.flipkart.com/orient-electric-ujala-air-1-star-1200-mm-3-blade-ceiling-fan/p/itm86c3958e8a4e0",
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1200-mm-3-blade-ceiling-fan/p/itme0dfe1a5d5737"
]

# 🎯 Set your desired max price for each product (in ₹)
target_prices = {
    product_urls[0]: 1300,
    product_urls[1]: 1200,
    product_urls[2]: 1300
}

# 📤 Send Telegram message (async)
async def send_telegram_message(product_url, price):
    try:
        message = (
            "⚠️〽️ *Price Drop Alert!*\n\n"
            "🔥💰 A tracked product just changed price!\n\n"
            f"🛒⏩ [View Product]({product_url})\n"
            f"💸🤑 *New Price:* {price}\n\n"
            "✅🛍️ Buy fast!"
        )
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
    except Exception as e:
        print(f"⚠️ Telegram send error: {e}")

# 🌐 Launch headless browser
def get_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

# 🧠 Extract price using fallback regex
def extract_price_from_page_source(page_source):
    match = re.search(r'₹\s?[0-9,]+', page_source)
    if match:
        return match.group()
    return None

# 💵 Convert ₹1,399 → 1399
def parse_price(price_str):
    return int(re.sub(r"[^\d]", "", price_str))

# 🧪 Check prices
async def check_price():
    browser = get_browser()
    for url in product_urls:
        print(f"Checking: {url}")
        try:
            browser.get(url)
            time.sleep(2)
            print("🟡 Page title:", browser.title)

            try:
                price_elem = browser.find_element("css selector", "._30jeq3")
                price_str = price_elem.text
            except NoSuchElementException:
                print("⚠️ Falling back to regex scan")
                price_str = extract_price_from_page_source(browser.page_source)

            if price_str:
                price_int = parse_price(price_str)
                print(f"✅ Price for:\n{url}\nis ₹{price_int}")

                if price_int <= target_prices[url]:
                    await send_telegram_message(url, price_int)
                else:
                    print(f"ℹ️ Price ₹{price_int} is above your target ₹{target_prices[url]} — no alert.")
            else:
                print(f"❌ Could not extract price for {url}")
        except Exception as e:
            print(f"❌ Could not get price from {url}\nReason: {e}")
    browser.quit()

# ▶️ Run the script
if __name__ == "__main__":
    asyncio.run(check_price())
