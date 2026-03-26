from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route("/")
def home():
    return "Webhook is live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}

    symbol = data.get("symbol", "Unknown")
    side = data.get("side", "Unknown")
    timeframe = data.get("timeframe", "Unknown")
    price = data.get("price", "Unknown")

    message = f"""🚨 TRADE ALERT 🚨
Symbol: {symbol}
Side: {side}
Timeframe: {timeframe}
Price: {price}"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, json=payload, timeout=10)

    return {"status": "ok"}, 200
