from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = "8729249832:AAESzqC79mtTkl5BZyBhzKTStow2a9RLubM"
CHAT_ID = "7963887087"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    symbol = data.get("symbol", "Unknown")
    side = data.get("side", "Unknown")
    timeframe = data.get("timeframe", "")
    price = data.get("price", "")

    message = f"""
🚨 TRADE ALERT 🚨
Symbol: {symbol}
Side: {side}
Timeframe: {timeframe}
Price: {price}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, json=payload)

    return {"status": "ok"}

if __name__ == '__main__':
    app.run()