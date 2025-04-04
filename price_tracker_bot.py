import requests
from bs4 import BeautifulSoup
from telegram import Bot
import time

# Replace with your actual bot token and chat ID
TELEGRAM_TOKEN = 'YOUR_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'

bot = Bot(token=TELEGRAM_TOKEN)

# URL and target price list
products = {
    "https://www.flipkart.com/sample-product-url/p/itm123456": 35000  # Change URL & price
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def check_price():
    for url, target_price in products.items():
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.find('span', {'class': 'B_NuCI'}).text.strip()
            price_text = soup.find('div', {'class': '_30jeq3 _16Jk6d'}).text.strip()

            current_price = int(price_text.replace('₹', '').replace(',', ''))

            if current_price <= target_price:
                message = f"🔥 *Price Drop Alert!*\n\n*{title}*\nPrice: ₹{current_price} (Target: ₹{target_price})\n\n[View Product]({url})"
                bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
            else:
                print(f"No drop: {title} ₹{current_price}")
        except Exception as e:
            print(f"Error checking price for {url}: {e}")

if __name__ == '__main__':
    check_price()
