import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Bot

API_TOKEN = "7866528662:AAHjd1BAefRm0RBYvy_KPql23HqMAx__VNI"
CHAT_ID = "163447880"

bot = Bot(token=API_TOKEN)

product_urls = [
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1-1200-mm-3-blade-ceiling-fan/p/itmfaf147854846b",
    "https://www.flipkart.com/flipkart-smartbuy-dlx-n1-1200-mm-3-blade-ceiling-fan/p/itm7d3e56c6e2f54",
    "https://www.flipkart.com/usha-bloom-daffodil-1250-mm-3-blade-ceiling-fan/p/itmdghkpxa2j7zvh"
]

def get_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def get_price(browser, url):
    browser.get(url)
    browser.implicitly_wait(10)

    try:
        price_element = browser.find_element(By.CSS_SELECTOR, "._30jeq3")
        return price_element.text
    except Exception as e:
        raise Exception(f"Could not extract price: {str(e)}")

async def send_telegram_alert(bot, message):
    await bot.send_message(chat_id=CHAT_ID, text=message)

def check_price():
    browser = get_browser()
    for url in product_urls:
        print(f"Checking: {url}")
        try:
            price = get_price(browser, url)
            print(f"✅ Price for {url}: {price}")
            asyncio.run(send_telegram_alert(bot, f"🟢 Price for:\n{url}\n💰 {price}"))
        except Exception as e:
            print(f"❌ Could not get price from {url}\nReason: {e}")
            asyncio.run(send_telegram_alert(bot, f"⚠️ Couldn't fetch price for:\n{url}"))
    browser.quit()

if __name__ == "__main__":
    check_price()
