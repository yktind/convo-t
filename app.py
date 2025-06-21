
from flask import Flask, request, render_template_string
import requests
import time
import json
import uuid

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>Messenger GraphQL Auto Sender</title>
  <style>
    body { font-family: Arial; padding: 20px; background: #f0f0f0; }
    form { background: white; padding: 20px; border-radius: 12px; max-width: 500px; margin: auto; box-shadow: 0 0 8px rgba(0,0,0,0.1); }
    input, textarea, select { width: 100%; padding: 10px; margin-top: 10px; border-radius: 6px; border: 1px solid #ccc; }
    button { padding: 10px; background: #4CAF50; color: white; border: none; border-radius: 6px; margin-top: 10px; cursor: pointer; }
    button:hover { background: #45a049; }
  </style>
</head>
<body>
  <h2>📨 Messenger Auto Bot (GraphQL)</h2>
  <form method='POST' enctype='multipart/form-data'>
    <label>🔑 VinhTool Token:</label>
    <input type='text' name='token' required>

    <label>🎯 Target UID:</label>
    <input type='text' name='uid' required>

    <label>⏱️ Delay (seconds):</label>
    <input type='number' name='delay' value='2' step='0.5'>

    <label>💬 Message Type:</label>
    <select name='message_source' onchange='toggleSource(this.value)'>
      <option value='text'>Manual Message</option>
      <option value='file'>Upload .txt File</option>
    </select>

    <div id='manualMsg'>
      <label>✍️ Message Text:</label>
      <textarea name='message_text' rows='4'></textarea>
    </div>

    <div id='fileMsg' style='display:none;'>
      <label>📁 Upload .txt (1 message per line):</label>
      <input type='file' name='message_file' accept='.txt'>
    </div>

    <button type='submit'>🚀 Start Sending</button>
  </form>

  <script>
    function toggleSource(value) {
      document.getElementById("manualMsg").style.display = value === "text" ? "block" : "none";
      document.getElementById("fileMsg").style.display = value === "file" ? "block" : "none";
    }
  </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        token = request.form["token"]
        uid = request.form["uid"]
        delay = float(request.form["delay"])
        source = request.form["message_source"]

        if source == "file":
            message_file = request.files["message_file"]
            messages = message_file.read().decode("utf-8").splitlines()
        else:
            messages = [request.form["message_text"]]

        results = ""
        for msg in messages:
            status = send_graphql_message(token, uid, msg)
            results += f"✅ Sent: {msg[:30]}... → {status}<br>"
            time.sleep(delay)

        return f"<h3>Result:</h3><p>{results}</p><a href='/'>⬅️ Go Back</a>"

    return render_template_string(HTML_PAGE)


def send_graphql_message(token, recipient_id, message):
    url = "https://graph.facebook.com/graphql"
    headers = {
        "Authorization": f"OAuth {token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Facebook Android",
        "X-FB-Friendly-Name": "MessengerGraphQLSendMessageMutation",
        "X-FB-Connection-Type": "mobile.LTE",
    }

    message_id = str(uuid.uuid4())
    variables = {
        "id": recipient_id,
        "message": message,
        "client_mutation_id": message_id,
        "actor_id": recipient_id,
        "messaging_tag": "ACCOUNT_UPDATE",
        "message_type": "MESSAGE_TAG"
    }

    form_data = {
        "av": recipient_id,
        "__user": recipient_id,
        "__a": "1",
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": "MessengerGraphQLSendMessageMutation",
        "variables": json.dumps(variables),
        "doc_id": "5301538573184946"
    }

    try:
        response = requests.post(url, headers=headers, data=form_data)
        return f"{response.status_code} - OK" if response.ok else f"{response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
  
