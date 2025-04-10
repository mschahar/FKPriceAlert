import asyncio
import re
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
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1200-mm-3-blade-ceiling-fan/p/itme0dfe1a5d5737",
    #"https://www.flipkart.com/rr-signature-josh-eco-star-rated-bee-certified-energy-efficient-52-watt-high-speed-1-star-1200-mm-3-blade-ceiling-fan/p/itm5c91ceb2beb19"
]

target_prices = {
    product_urls[0]: 1100,
    product_urls[1]: 1100,
    product_urls[2]: 1100,
    #product_urls[3]: 1200
}

# 📤 Send Telegram message
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

# 🚀 Headless browser setup
def get_browser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 🧠 Extract price using latest Flipkart class
def extract_main_price(driver, wait):
    try:
        price_elem = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.Nx9bqj.CxhGGd'))
        )
        price_str = price_elem.text.strip()
        price = int(re.sub(r"[^\d]", "", price_str))
        print(f"✅ Price from new Flipkart class: ₹{price}")
        return price
    except Exception:
        pass

    # Fallback to older class
    try:
        price_elem = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div._30jeq3'))
        )
        price_str = price_elem.text.strip()
        price = int(re.sub(r"[^\d]", "", price_str))
        print(f"✅ Price from fallback class: ₹{price}")
        return price
    except Exception:
        return None

# 💡 Handle "Or Pay ₹1139 + 60" style prices
def extract_price_with_coins(driver):
    try:
        elems = driver.find_elements(By.XPATH, "//*[contains(text(),'Or Pay ₹')]")
        for elem in elems:
            text = elem.text.strip()
            match = re.search(r'Or Pay ₹([\d,]+)\s*\+\s*(\d+)', text)
            if match:
                cash = int(match.group(1).replace(',', ''))
                coins = int(match.group(2))
                total = cash + coins
                print(f"💡 Coin-based pricing: ₹{cash} + {coins} coins = ₹{total}")
                return total
    except:
        pass
    return None

# Regex fallback
def extract_price_from_page_source(page_source):
    match = re.search(r'₹\s?[0-9,]+', page_source)
    if match:
        return int(re.sub(r"[^\d]", "", match.group()))
    return None

# 📦 Main logic
async def check_price():
    browser = get_browser()
    wait = WebDriverWait(browser, 10)

    for url in product_urls:
        print(f"\n🔍 Checking: {url}")
        try:
            browser.get(url)

            # 1. Try coin-based
            price = extract_price_with_coins(browser)

            # 2. Try main classes
            if price is None:
                price = extract_main_price(browser, wait)

            # 3. Fallback regex
            if price is None:
                price = extract_price_from_page_source(browser.page_source)
                if price:
                    print(f"🧪 Regex fallback price: ₹{price}")

            if price:
                if price <= target_prices[url]:
                    print(f"🎯 Price ₹{price} is within target → alerting.")
                    await send_telegram_message(url, f"₹{price}")
                else:
                    print(f"ℹ️ ₹{price} is above target of ₹{target_prices[url]} — no alert.")
            else:
                print("❌ Could not extract price.")

        except Exception as e:
            print(f"❌ Error checking {url}:\n{e}")

    browser.quit()

# ▶️ Run the script
if __name__ == "__main__":
    asyncio.run(check_price())
