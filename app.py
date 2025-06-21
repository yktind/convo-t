from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Facebook Messenger Auto Sender</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      padding: 20px;
      background: #f2f2f2;
    }
    h1 { color: #333; }
    form {
      background: #fff;
      padding: 20px;
      border-radius: 12px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
      max-width: 500px;
      margin: auto;
    }
    input, textarea, select {
      width: 100%;
      padding: 10px;
      margin-top: 10px;
      margin-bottom: 15px;
      border: 1px solid #ccc;
      border-radius: 6px;
    }
    button {
      padding: 10px;
      background: #4CAF50;
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
    }
    button:hover {
      background: #45a049;
    }
  </style>
</head>
<body>
  <h1>📨 Facebook Messenger Bot</h1>
  <form method="POST" enctype="multipart/form-data">
    <label>🔑 VinhTool Token:</label>
    <input type="text" name="token" required>

    <label>🎯 Target UID (User or Group Chat):</label>
    <input type="text" name="uid" required>

    <label>⏱️ Delay between messages (seconds):</label>
    <input type="number" name="delay" value="2" min="1" step="0.5" required>

    <label>💬 Message Type:</label>
    <select name="message_source" onchange="toggleSource(this.value)">
      <option value="text">Manual Message</option>
      <option value="file">Upload .txt File</option>
    </select>

    <div id="manualMsg">
      <label>✍️ Message Text:</label>
      <textarea name="message_text" rows="4"></textarea>
    </div>

    <div id="fileMsg" style="display:none;">
      <label>📂 Upload .txt file (1 message per line):</label>
      <input type="file" name="message_file" accept=".txt">
    </div>

    <button type="submit">🚀 Start Messaging</button>
  </form>

  <script>
    function toggleSource(value) {
      document.getElementById("manualMsg").style.display = value === "text" ? "block" : "none";
      document.getElementById("fileMsg").style.display = value === "file" ? "block" : "none";
    }
  </script>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        token = request.form["token"]
        recipient_id = request.form["uid"]
        delay = float(request.form["delay"])
        message_source = request.form.get("message_source")

        if message_source == "file":
            message_file = request.files["message_file"]
            messages = message_file.read().decode("utf-8").splitlines()
        else:
            messages = [request.form["message_text"]]

        result_log = ""
        for msg in messages:
            status = send_message(token, recipient_id, msg)
            result_log += f"✅ Sent: {msg} → {status}<br>"
            time.sleep(delay)

        return f"<h3>Result:</h3><p>{result_log}</p><a href='/'>⬅️ Go Back</a>"

    return render_template_string(HTML_PAGE)

def send_message(token, recipient_id, message):
    url = "https://b-graph.facebook.com/messaging/send/"
    headers = {
        "Authorization": f"OAuth {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message},
        "messaging_type": "MESSAGE_TAG",
        "tag": "ACCOUNT_UPDATE"
    }

    response = requests.post(url, json=payload, headers=headers)
    return f"{response.status_code} - {response.text}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
  
