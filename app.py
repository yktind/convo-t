# ✅ Final app.py (Flask web app to send Facebook Messenger message using token)

from flask import Flask, request, redirect, Response
import threading, time, requests, random

app = Flask(__name__)

access_token = ""
thread_id = ""
delay = 5
message_text = ""
is_running = False
stop_flag = False

def send_message(token, thread_id, message):
    url = "https://graph.facebook.com/v19.0/me/messages"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "recipient": {"thread_key": thread_id},
        "message": {"text": message},
        "messaging_type": "MESSAGE_TAG",
        "tag": "ACCOUNT_UPDATE"
    }
    res = requests.post(url, headers=headers, json=payload)
    print("Status:", res.status_code)
    print("Response:", res.text[:300])
    if 'message_id' in res.text:
        print("✅ Message sent!")
    else:
        print("❌ Not sent.")

def bot():
    global is_running, stop_flag
    is_running = True
    stop_flag = False
    while not stop_flag:
        send_message(access_token, thread_id, message_text)
        time.sleep(delay)
    is_running = False

HTML = '''
<!DOCTYPE html><html><head><title>FB Messenger Bot</title>
<style>
body {
  font-family: Arial; background: #111; color: #eee; text-align: center;
}
input, textarea, button {
  padding: 10px; margin: 6px; border-radius: 6px; border: none;
}
button { font-weight: bold; background: linear-gradient(to right, #0af, #08f); color: white; }
</style></head>
<body>
<h2>📬 FB Messenger Token Sender</h2>
<form method="POST">
<input name="token" placeholder="Access Token" size="70"><br>
<input name="uid" placeholder="Thread ID (UID)"><br>
<textarea name="message" placeholder="Enter message here..." rows="4" cols="50"></textarea><br>
<input type="number" name="delay" value="5"> Delay (sec)<br>
<button type="submit">Start</button></form>
<form action="/stop"><button>Stop</button></form>
</body></html>
'''

@app.route("/", methods=["GET", "POST"])
def home():
    global access_token, thread_id, delay, message_text
    if request.method == "POST":
        access_token = request.form['token']
        thread_id = request.form['uid']
        message_text = request.form['message']
        delay = int(request.form['delay'])
        threading.Thread(target=bot).start()
        return redirect("/")
    return Response(HTML, mimetype="text/html")

@app.route("/stop")
def stop():
    global stop_flag
    stop_flag = True
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
  
