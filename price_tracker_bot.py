import requests
from bs4 import BeautifulSoup
from telegram import Bot
import os
import time

# Load Telegram credentials from environment variables
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

bot = Bot(token=TELEGRAM_TOKEN)

# 🔗 Flipkart product URLs and their target prices (in ₹)
products = {
    "https://dl.flipkart.com/s/xm1vSYNNNN": 1099,
    "https://dl.flipkart.com/s/xmm2lyNNNN": 1099,
    "https://dl.flipkart.com/s/kSFcPAuuuN": 1099
}

# Mimic browser headers to avoid blocks
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
}


def get_with_retry(url, retries=3, delay=5):
    """Try to fetch the URL with retry logic."""
    for attempt in range(1, retries + 1):
        try:
            return requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt} failed for {url}\nReason: {e}")
            time.sleep(delay)
    raise Exception(f"Failed to fetch {url} after {retries} retries.")


def check_price():
    for url, target_price in products.items():
        try:
            response = get_with_retry(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.find('span', class_='B_NuCI')
            price_tag = soup.find('div', class_='_30jeq3 _16Jk6d')

            if not title or not price_tag:
                print(f"❌ Could not extract price/title from: {url}")
                continue

            title = title.text.strip()
            current_price = int(price_tag.text.strip().replace('₹', '').replace(',', ''))

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
            print(f"\n🔴 Error while checking:\n{url}\nError: {e}\n")


if __name__ == '__main__':
    check_price()
