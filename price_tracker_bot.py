import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Bot

# Load Telegram bot token and chat ID
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
bot = Bot(token=TELEGRAM_TOKEN)

# Flipkart product URLs and target price
products = {
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1-1200-mm-3-blade-ceiling-fan/p/itmfaf147854846b": 1099,
    "https://www.flipkart.com/orient-electric-ujala-air-1-star-1200-mm-3-blade-ceiling-fan/p/itm86c3958e8a4e0": 1099,
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1200-mm-3-blade-ceiling-fan/p/itme0dfe1a5d5737": 1099,
}

# Setup headless Chrome browser
def get_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 Chrome/123.0 Safari/537.36")

    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    return browser

# Price checker using Selenium
def check_price():
    browser = get_browser()

    for url, target_price in products.items():
        try:
            browser.get(url)
            time.sleep(5)  # Wait for full load

            title_el = browser.find_element(By.CLASS_NAME, "B_NuCI")
            price_el = browser.find_element(By.CLASS_NAME, "_30jeq3")

            title = title_el.text.strip()
            current_price = int(price_el.text.replace("₹", "").replace(",", "").strip())

            print(f"✅ {title} — ₹{current_price}")

            if current_price <= target_price:
                message = (
                    f"🔥 *Price Drop Alert!*\n\n"
                    f"*{title}*\n"
                    f"Price: ₹{current_price} (Target: ₹{target_price})\n\n"
                    f"[🔗 Buy Now]({url})"
                )
                bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')

        except Exception as e:
            print(f"\n🔴 Error checking {url}\nReason: {e}\n")

    browser.quit()

# Run
if __name__ == '__main__':
    check_price()
