
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
  <title>Messenger Bot (GraphQL Working)</title>
  <style>
    body { font-family: Arial; padding: 20px; background: #f4f4f4; }
    form { background: white; padding: 20px; border-radius: 10px; max-width: 500px; margin: auto; box-shadow: 0 0 8px rgba(0,0,0,0.1); }
    input, textarea, select { width: 100%; padding: 10px; margin-top: 10px; border-radius: 5px; border: 1px solid #ccc; }
    button { padding: 10px; background: #4CAF50; color: white; border: none; border-radius: 5px; margin-top: 10px; cursor: pointer; }
    button:hover { background: #45a049; }
  </style>
</head>
<body>
  <h2>ðŸ“¨ Messenger Bot - GraphQL Method</h2>
  <form method='POST'>
    <label>ðŸ”‘ VinhTool Token:</label>
    <input type='text' name='token' required>

    <label>ðŸŽ¯ Target UID:</label>
    <input type='text' name='uid' required>

    <label>â±ï¸ Delay (seconds):</label>
    <input type='number' name='delay' value='2' step='0.5'>

    <label>âœï¸ Message:</label>
    <textarea name='message_text' rows='4'></textarea>

    <button type='submit'>ðŸš€ Send Message</button>
  </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        token = request.form["token"]
        uid = request.form["uid"]
        message = request.form["message_text"]
        delay = float(request.form["delay"])
        status = send_graphql_message(token, uid, message)
        time.sleep(delay)
        return f"<h3>âœ… Result:</h3><p>{status}</p><a href='/'>â¬…ï¸ Go Back</a>"
    return render_template_string(HTML_PAGE)

def send_graphql_message(token, recipient_id, message):
    url = "https://graph.facebook.com/graphql"
    headers = {
        "Authorization": f"OAuth {token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Facebook Android",
        "X-FB-Friendly-Name": "MessengerGraphQLSendMessageMutation",
        "X-FB-Connection-Type": "mobile.LTE"
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
        "doc_id": "7714890518579626"
    }
    try:
        response = requests.post(url, headers=headers, data=form_data)
        if response.ok:
            return f"âœ… Sent: {message} â†’ {response.status_code} - OK"
        else:
            return f"âŒ Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"âŒ Exception: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
