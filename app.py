from flask import Flask, request, redirect, Response
import threading, time, random, requests
from bs4 import BeautifulSoup

app = Flask(__name__)
is_running = False
stop_flag = False
thread = None

bot_config = {
    "cookie": "",
    "uid": "",
    "delay": 10,
    "messages": []
}

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Facebook AutoMessenger</title>
  <style>
    body {
      background-image: url('https://wallpapercave.com/wp/wp5128415.jpg');
      background-size: cover;
      color: white;
      font-family: Arial, sans-serif;
      padding: 40px;
    }
    form {
      background: rgba(0, 0, 0, 0.6);
      padding: 20px;
      border-radius: 15px;
    }
    input, button {
      padding: 10px;
      width: 100%;
      margin: 10px 0;
      border-radius: 10px;
      border: none;
    }
    button {
      background: linear-gradient(to right, #00c6ff, #0072ff);
      color: white;
      font-weight: bold;
      transition: 0.3s ease;
    }
    button:hover {
      transform: scale(1.05);
      background: linear-gradient(to right, #0072ff, #00c6ff);
    }
    .stop-btn {
      background: crimson;
      color: white;
    }
  </style>
</head>
<body>
  <h2>📨 Facebook Messenger Auto Sender</h2>
  <form method="POST" enctype="multipart/form-data">
    <label>🍪 Facebook Cookie:</label>
    <input type="text" name="cookie" required>

    <label>🎯 Target UID / Thread ID:</label>
    <input type="text" name="uid" required>

    <label>📄 Upload .txt Message File:</label>
    <input type="file" name="message_file" accept=".txt" required>

    <label>⏱️ Delay (in seconds):</label>
    <input type="number" name="delay" value="10" min="1">

    <button type="submit">🚀 Start Sending</button>
  </form>

  <form action="/stop">
    <button class="stop-btn">🛑 Stop</button>
  </form>
</body>
</html>
'''

def get_fb_dtsg(cookie):
    try:
        res = requests.get("https://mbasic.facebook.com/messages", headers={
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0"
        })
        soup = BeautifulSoup(res.text, "html.parser")
        token = soup.find("input", {"name": "fb_dtsg"})
        if token:
            return token["value"]
    except:
        return None

def send_message(cookie, thread_id, message, fb_dtsg):
    try:
        url = f"https://mbasic.facebook.com/messages/thread/{thread_id}"
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Cookie": cookie
        }
        res = session.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        form = soup.find("form")
        if not form:
            print("❌ Failed to load message form")
            return

        action_url = form["action"]
        inputs = form.find_all("input")
        data = {}
        for input_tag in inputs:
            name = input_tag.get("name")
            value = input_tag.get("value", "")
            if name:
                data[name] = value

        data["body"] = message
        send = session.post("https://mbasic.facebook.com" + action_url, headers=headers, data=data)
        print("✅ Message sent:", message)
    except Exception as e:
        print("❌ Error:", e)

def bot_thread():
    global stop_flag, is_running
    fb_dtsg = get_fb_dtsg(bot_config["cookie"])
    if not fb_dtsg:
        print("❌ Could not fetch fb_dtsg. Invalid cookie?")
        is_running = False
        return

    while not stop_flag:
        msg = random.choice(bot_config["messages"])
        send_message(bot_config["cookie"], bot_config["uid"], msg, fb_dtsg)
        time.sleep(bot_config["delay"])
    is_running = False

@app.route("/", methods=["GET", "POST"])
def index():
    global bot_config, is_running, stop_flag, thread

    if request.method == "POST":
        bot_config["cookie"] = request.form.get("cookie")
        bot_config["uid"] = request.form.get("uid")
        bot_config["delay"] = int(request.form.get("delay", "10"))
        file = request.files["message_file"]
        bot_config["messages"] = [line.strip() for line in file.read().decode("utf-8").splitlines() if line.strip()]

        if not is_running:
            stop_flag = False
            thread = threading.Thread(target=bot_thread)
            thread.start()
            is_running = True

        return redirect("/")

    return Response(HTML_PAGE, mimetype='text/html')

@app.route("/stop")
def stop():
    global stop_flag, is_running
    stop_flag = True
    is_running = False
    return redirect("/")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
    
