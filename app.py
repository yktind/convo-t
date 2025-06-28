from flask import Flask, request, redirect, Response
import threading
import requests
import time
import random
from bs4 import BeautifulSoup

app = Flask(__name__)

# Variables
app_cookie = ""
app_uid = ""
app_delay = 10
app_messages = []
app_running = False
app_stop = False
app_thread = None

HTML = '''<html>
<head><title>FB Bot</title></head>
<body>
<h2>Facebook Bot</h2>
<form method="POST" enctype="multipart/form-data">
  Cookie:<br><input type="text" name="cookie"><br>
  UID:<br><input type="text" name="uid"><br>
  Delay:<br><input type="number" name="delay" value="5"><br>
  .txt File:<br><input type="file" name="message_file"><br>
  <button type="submit">Start</button>
</form>
<form action="/stop"><button>Stop</button></form>
</body>
</html>'''

def get_token(cook):
    try:
        r = requests.get("https://mbasic.facebook.com/messages", headers={
            "Cookie": cook,
            "User-Agent": "Mozilla/5.0"
        })
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.find("input", {"name": "fb_dtsg"}).get("value")
    except:
        return None

def send_msg(cook, uid, msg, token):
    try:
        url = f"https://mbasic.facebook.com/messages/thread/{uid}"
        s = requests.Session()
        h = {"Cookie": cook, "User-Agent": "Mozilla/5.0"}
        res = s.get(url, headers=h)
        soup = BeautifulSoup(res.text, "html.parser")
        form = soup.find("form")
        if not form: return
        action = form["action"]
        inputs = form.find_all("input")
        data = {i.get("name"): i.get("value", "") for i in inputs if i.get("name")}
        data["body"] = msg
        s.post("https://mbasic.facebook.com" + action, headers=h, data=data)
        print("✅", msg)
    except Exception as e:
        print("❌", e)

def run_bot():
    global app_cookie, app_uid, app_delay, app_messages, app_stop, app_running
    token = get_token(app_cookie)
    if not token:
        print("❌ Invalid cookie")
        app_running = False
        return
    while not app_stop:
        m = random.choice(app_messages)
        send_msg(app_cookie, app_uid, m, token)
        time.sleep(app_delay)
    app_running = False

@app.route("/", methods=["GET", "POST"])
def main():
    global app_cookie, app_uid, app_delay, app_messages, app_stop, app_running, app_thread
    if request.method == "POST":
        app_cookie = request.form["cookie"]
        app_uid = request.form["uid"]
        app_delay = int(request.form["delay"])
        file = request.files["message_file"]
        app_messages = [line.strip() for line in file.read().decode().splitlines() if line.strip()]
        if not app_running:
            app_stop = False
            app_thread = threading.Thread(target=run_bot)
            app_thread.start()
            app_running = True
        return redirect("/")
    return Response(HTML, mimetype='text/html')

@app.route("/stop")
def stop():
    global app_stop, app_running
    app_stop = True
    app_running = False
    return redirect("/")

if __name__ == "__main__":
    app.run(port=5000)
      
