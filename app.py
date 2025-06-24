from flask import Flask, request
import os, time, threading, random
import requests
from instagrapi import Client
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

running = False

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
  <title>Automation Panel</title>
  <style>
    body {
      background: linear-gradient(135deg, #1e1e2f, #1f1f3a);
      color: white;
      font-family: sans-serif;
      text-align: center;
      padding: 40px;
    }
    input, button {
      padding: 10px;
      margin: 8px;
      border: none;
      border-radius: 10px;
      width: 280px;
    }
    button {
      background: linear-gradient(to right, #667eea, #764ba2);
      color: white;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <h2>📱 Instagram + Facebook Messenger Bot</h2>
  <form method="POST" enctype="multipart/form-data">
    <h3>🔵 Instagram Login</h3>
    <input name="ig_user" placeholder="Instagram Username"><br>
    <input type="password" name="ig_pass" placeholder="Instagram Password"><br>
    <input name="ig_target" placeholder="Target Instagram Thread ID"><br>

    <h3>🔵 Facebook Messenger</h3>
    <input name="fb_token" placeholder="VinhTool Token"><br>
    <input name="fb_uid" placeholder="Target UID / Thread ID"><br>

    <h3>📝 Upload Messages (.txt)</h3>
    <input type="file" name="message_file"><br>
    <input name="delay" placeholder="Delay (sec)" type="number"><br>

    <button type="submit" name="action" value="start">🚀 Start</button>
    <button type="submit" name="action" value="stop">🛑 Stop</button>
  </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    global running
    if request.method == "POST":
        action = request.form.get("action")
        if action == "stop":
            running = False
            return "🛑 Bot stopped."

        fb_token = request.form.get("fb_token")
        fb_uid = request.form.get("fb_uid")
        ig_user = request.form.get("ig_user")
        ig_pass = request.form.get("ig_pass")
        ig_target = request.form.get("ig_target")
        delay = int(request.form.get("delay", 5))

        file = request.files["message_file"]
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        with open(filepath, "r", encoding="utf-8") as f:
            messages = f.read().splitlines()

        running = True
        threading.Thread(target=bot_runner, args=(fb_token, fb_uid, ig_user, ig_pass, ig_target, messages, delay)).start()
        return "✅ Bot Started. You may close this tab."

    return HTML_UI

def bot_runner(fb_token, fb_uid, ig_user, ig_pass, ig_target, messages, delay):
    global running
    ig = Client()
    try:
        ig.login(ig_user, ig_pass)
        print("✅ Instagram login successful.")
    except Exception as e:
        print("❌ Instagram login failed:", e)

    while running:
        try:
            msg = random.choice(messages)

            # Send Instagram message
            if ig_target:
                try:
                    ig.direct_send([msg], thread_ids=[ig_target])
                    print(f"📩 IG Sent: {msg}")
                except Exception as e:
                    print("IG Send Error:", e)

            # Send Facebook message
            if fb_token and fb_uid:
                try:
                    send_fb_message(fb_token, fb_uid, msg)
                    print(f"📤 FB Sent: {msg}")
                except Exception as e:
                    print("FB Send Error:", e)

            time.sleep(delay)
        except Exception as e:
            print("Loop Error:", e)
            time.sleep(5)

def send_fb_message(token, uid, msg):
    headers = {
        'Authorization': f'OAuth {token}',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0'
    }
    data = {
        'recipient': '{"thread_fbid":"' + uid + '"}',
        'message': msg,
        'messaging_type': 'RESPONSE'
    }
    requests.post("https://graph.facebook.com/v17.0/me/messages", headers=headers, data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
