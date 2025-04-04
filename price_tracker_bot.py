import requests
from bs4 import BeautifulSoup
from telegram import Bot
import os

# Get credentials from GitHub Secrets (Actions env variables)
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

bot = Bot(token=TELEGRAM_TOKEN)

# Flipkart products to track: {url: target_price}
products = {
    "https://www.flipkart.com/orient-electric-ujala-air-bee-star-rated-1-1200-mm-3-blade-ceiling-fan/p/itmfaf147854846b": 1099,
    "https://www.flipkart.com/orient-electric-ujala-air-1-star-1200-mm-3-blade-ceiling-fan/p/itm86c3958e8a4e0": 1099
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def check_price():
    for url, target_price in products.items():
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')

            title = soup.find('span', {'class': 'B_NuCI'}).text.strip()
            price = soup.find('div', {'class': '_30jeq3 _16Jk6d'}).text.strip()
            current_price = int(price.replace('₹', '').replace(',', ''))

            print(f"{title} - ₹{current_price}")

            if current_price <= target_price:
                msg = f"🔥 *Price Drop Alert!*\n\n*{title}*\nPrice: ₹{current_price} (Target: ₹{target_price})\n\n[🔗 Buy Now]({url})"
                bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown')
        except Exception as e:
            print(f"Error with {url}: {e}")

if __name__ == '__main__':
    check_price()
