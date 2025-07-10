from flask import Flask, request
import requests

app = Flask(__name__)
PAGE_TOKEN = "EAABwzLixnjYBPBnFF8I5izQJPuIQ50MgtSDisH5DuiUym4qvgN24tDxdxpLZB1AfNfxZBb2TYcCCWwc8C9byjALkYvZBduEZAZACN6UbnkQ4mAAViYVBHyaVd6UsEqZAROOGaVBUZCFQ3OLy63PiyXtZA8nN7D0mM5iP2HZAY7iGHL3M4ZC4zYhfMntU9y1nJlIscVhZCpU7rkZD"

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.verify_token") == "ayush_verify":
        return request.args.get("hub.challenge")
    return "Verification failed"

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    for entry in data["entry"]:
        for msg in entry["messaging"]:
            sender = msg["sender"]["id"]
            if msg.get("message"):
                send_reply(sender, "ðŸ‘‹ Hello! This is Auto Reply Bot.")
    return "ok", 200

def send_reply(user_id, message):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_TOKEN}"
    payload = {
        "recipient": {"id": user_id},
        "message": {"text": message}
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
