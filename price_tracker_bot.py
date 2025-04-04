import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Bot

# Telegram Setup
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
bot = Bot(token=TELEGRAM_TOKEN)

# Flipkart product URLs
urls = [
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1-1200-mm-3-blade-ceiling-fan/p/itmfaf147854846b",
    "https://www.flipkart.com/orient-electric-ujala-air-1-star-1200-mm-3-blade-ceiling-fan/p/itm86c3958e8a4e0",
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1200-mm-3-blade-ceiling-fan/p/itme0dfe1a5d5737"
]

TARGET_PRICE = 1099

def get_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    return webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)

def get_price(browser, url):
    try:
        browser.get(url)
        wait = WebDriverWait(browser, 10)
        price_element = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "._30jeq3, .aMaAEs .dyC4hf, .aMaAEs ._16Jk6d")
        ))
        price_text = price_element.text.strip().replace("₹", "").replace(",", "")
        return int(float(price_text))
    except Exception as e:
        print(f"❌ Could not get price from {url}")
        print(f"Reason: {e}")
        return None

def check_price():
    browser = get_browser()
    for url in urls:
        print(f"Checking: {url}")
        price = get_price(browser, url)
        if price:
            print(f"✅ Price found: ₹{price}")
            if price <= TARGET_PRICE:
                bot.send_message(chat_id=CHAT_ID, text=f"✅ Price Drop Alert!\n{url}\nCurrent Price: ₹{price}")
        else:
            bot.send_message(chat_id=CHAT_ID, text=f"⚠️ Couldn't fetch price for:\n{url}")
    browser.quit()

if __name__ == "__main__":
    check_price()
