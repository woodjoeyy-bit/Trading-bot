from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route("/")
def home():
    return "Webhook is live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    raw_body = request.get_data(as_text=True).strip()

    message = ""

    # Try to parse JSON first
    try:
        data = request.get_json(silent=True)

        if isinstance(data, dict) and data:
            # If TradingView sends structured JSON
            if "symbol" in data or "side" in data or "price" in data:
                symbol = data.get("symbol", "Unknown")
                side = data.get("side", "Unknown")
                timeframe = data.get("timeframe", "Unknown")
                price = data.get("price", "Unknown")

                message = (
                    f"🚨 TRADE ALERT 🚨\n"
                    f"Symbol: {symbol}\n"
                    f"Side: {side}\n"
                    f"Timeframe: {timeframe}\n"
                    f"Price: {price}"
                )
            else:
                # JSON exists but is not in the old expected format
                message = json.dumps(data, indent=2)
        else:
            # Not JSON, so treat it as plain text from Pine alert()
            message = raw_body if raw_body else "Received empty alert."
    except Exception:
        # If anything goes wrong, just forward the raw message
        message = raw_body if raw_body else "Received empty alert."

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, json=payload, timeout=10)

    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run()
