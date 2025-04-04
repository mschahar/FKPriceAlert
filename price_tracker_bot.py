import re
import time
import telegram
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ✅ Hardcoded Telegram details
TELEGRAM_TOKEN = "7866528662:AAHjd1BAefRm0RBYvy_KPql23HqMAx__VNI"
TELEGRAM_CHAT_ID = "163447880"

bot = telegram.Bot(token=TELEGRAM_TOKEN)

# ✅ Flipkart product URLs
urls = [
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1-1200-mm-3-blade-ceiling-fan/p/itmfaf147854846b",
    "https://www.flipkart.com/orient-electric-ujala-air-1-star-1200-mm-3-blade-ceiling-fan/p/itm86c3958e8a4e0",
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1200-mm-3-blade-ceiling-fan/p/itme0dfe1a5d5737"
]

def get_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def extract_price_from_page(source):
    soup = BeautifulSoup(source, 'html.parser')

    # ✅ Try multiple known selectors
    selectors = [
        "._30jeq3",
        "div._16Jk6d",
        "div._25b18c > div._30jeq3"
    ]

    for selector in selectors:
        el = soup.select_one(selector)
        if el and el.text.strip().startswith("₹"):
            return el.text.strip()

    # 🟡 Fallback to stricter regex
    match = re.search(r"₹[\s]*[0-9]{3,5}", source)
    if match:
        return match.group().strip()

    raise ValueError("Could not extract price")

def send_telegram_message(message):
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"⚠️ Telegram send error: {e}")

def check_price():
    browser = get_browser()
    for url in urls:
        try:
            print(f"Checking: {url}")
            browser.get(url)
            time.sleep(3)
            page_title = browser.title
            print(f"🟡 Page title: {page_title}")
            source = browser.page_source

            try:
                price = extract_price_from_page(source)
                print(f"✅ Price for:\n{url}\nis {price}")
                send_telegram_message(f"✅ {price} – {url}")
            except Exception as e:
                print(f"❌ Could not extract price from {url}\nReason: {e}")

        except Exception as e:
            print(f"❌ Error loading {url}\nReason: {e}")
    browser.quit()

if __name__ == "__main__":
    check_price()
