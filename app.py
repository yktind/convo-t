
from flask import Flask, request, redirect, Response
import threading, time, random, requests, json

app = Flask(__name__)

is_running = False
stop_flag = False
thread = None

fb_cookie = ""
target_uid = ""
delay_seconds = 5
messages = []

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
  <title>FB Messenger Auto Sender</title>
  <style>
    body {
      background: #0f2027;
      background: linear-gradient(to right, #2c5364, #203a43, #0f2027);
      color: white;
      font-family: Arial, sans-serif;
      padding: 40px;
    }
    form {
      background: rgba(255, 255, 255, 0.1);
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
  <h2>ðŸ“¨ Facebook Messenger Auto Sender (Web Cookie)</h2>
  <form method="POST" enctype="multipart/form-data">
    <label>ðŸª Facebook Cookie:</label>
    <input type="text" name="cookie" required>

    <label>ðŸŽ¯ Target Thread ID (Group or Inbox):</label>
    <input type="text" name="uid" required>

    <label>ðŸ“„ Upload .txt Message File:</label>
    <input type="file" name="message_file" accept=".txt" required>

    <label>â±ï¸ Delay (in seconds):</label>
    <input type="number" name="delay" value="5" min="1">

    <button type="submit">ðŸš€ Start Sending</button>
  </form>

  <form action="/stop">
    <button class="stop-btn">ðŸ›‘ Stop</button>
  </form>
</body>
</html>
'''

def send_graphql_message(cookie, thread_id, message):
    try:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0",
            "Cookie": cookie,
        }

        data = {
            "av": thread_id,
            "__user": thread_id,
            "__a": 1,
            "variables": json.dumps({
                "id": thread_id,
                "message": {"text": message},
                "client_mutation_id": "1"
            }),
            "doc_id": "5513683505370136"
        }

        response = requests.post(
            "https://www.facebook.com/api/graphql/",
            headers=headers,
            data=data
        )

        if response.status_code == 200:
            print("âœ… Sent:", message)
        else:
            print("âŒ Error:", response.text[:200])

    except Exception as e:
        print("âŒ Exception:", e)

def message_thread():
    global fb_cookie, target_uid, delay_seconds, messages, is_running, stop_flag
    while not stop_flag:
        msg = random.choice(messages)
        send_graphql_message(fb_cookie, target_uid, msg)
        time.sleep(delay_seconds)
    is_running = False

@app.route("/", methods=["GET", "POST"])
def index():
    global fb_cookie, target_uid, delay_seconds, messages, is_running, stop_flag, thread

    if request.method == "POST":
        fb_cookie = request.form.get("cookie")
        target_uid = request.form.get("uid")
        delay_seconds = int(request.form.get("delay", "5"))
        file = request.files["message_file"]
        messages = [line.strip() for line in file.read().decode("utf-8").splitlines() if line.strip()]

        if not is_running:
            stop_flag = False
            thread = threading.Thread(target=message_thread)
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
    app.run(port=5000)
