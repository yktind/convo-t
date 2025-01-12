import os
import time
import http.client
from flask import Flask, request, render_template, redirect, url_for, flash
from bs4 import BeautifulSoup as bs

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Flask server port
HOST = "0.0.0.0"
PORT = 5000


# Login Authentication using EAAB Token
def authenticate_with_token(token):
    try:
        conn = http.client.HTTPSConnection("graph.facebook.com")
        headers = {"Authorization": f"Bearer {token}"}
        conn.request("GET", "/me", headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
        conn.close()

        if response.status == 200:
            return True, f"Token Validated Successfully: {data}"
        else:
            return False, f"Token Invalid: {data}"

    except Exception as e:
        return False, f"Error during token validation: {str(e)}"


# Message Sender Function
def send_message(token, thread_id, message, user_agent):
    try:
        conn = http.client.HTTPSConnection("mbasic.facebook.com")
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": user_agent,
        }
        conn.request("GET", f"/messages/read/?tid={thread_id}", headers=headers)
        response = conn.getresponse()
        html = response.read().decode()

        # Parse the HTML for the form
        soup = bs(html, "html.parser")
        form = soup.find("form", method="post")
        if not form:
            return False, "Error: Unable to find message form."

        action_url = form["action"]
        payload = {inp["name"]: inp.get("value", "") for inp in form.find_all("input") if inp.get("name")}
        payload["body"] = message
        payload["send"] = "Send"

        # Send the message
        conn.request("POST", action_url, headers=headers, body="&".join([f"{k}={v}" for k, v in payload.items()]))
        send_response = conn.getresponse()
        conn.close()

        if "send" in send_response.getheader("Location", ""):
            return True, f"Message sent successfully to thread {thread_id}"
        else:
            return False, f"Error sending message to thread {thread_id}"

    except Exception as e:
        return False, f"Error: {str(e)}"


# Flask Routes

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        token = request.form.get("token")
        user_agent = request.form.get("user_agent")
        thread_id = request.form.get("thread_id")
        message_file = request.files.get("message_file")
        delay = int(request.form.get("delay", 5))

        # Validate inputs
        if not all([token, user_agent, thread_id, message_file]):
            flash("All fields are required.", "error")
            return redirect(url_for("index"))

        # Validate token
        is_valid, token_msg = authenticate_with_token(token)
        if not is_valid:
            flash(f"Token validation failed: {token_msg}", "error")
            return redirect(url_for("index"))

        # Process message file
        messages = message_file.read().decode().strip().split("\n")
        if not messages:
            flash("Message file is empty.", "error")
            return redirect(url_for("index"))

        # Send messages with delay
        for message in messages:
            success, msg = send_message(token, thread_id, message.strip(), user_agent)
            flash(msg, "success" if success else "error")
            time.sleep(delay)

        return redirect(url_for("index"))

    return render_template("index.html")


# HTML Template (render_template expects an HTML file in templates/)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Facebook Message Sender</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f5f5f5; color: #333; margin: 0; padding: 0; }
        .container { width: 60%; margin: 50px auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        h1 { text-align: center; color: #444; }
        form { display: flex; flex-direction: column; gap: 15px; }
        label { font-weight: bold; }
        input, textarea, select { padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
        button { padding: 10px 20px; background: #4CAF50; color: #fff; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #45a049; }
        .flash { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .success { background: #dff0d8; color: #3c763d; }
        .error { background: #f2dede; color: #a94442; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Facebook Message Sender</h1>
        {% with messages = get_flashed_messages(with_categories=True) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="flash {{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
        {% endwith %}
        <form method="POST" enctype="multipart/form-data">
            <label for="token">Facebook EAAB Token:</label>
            <input type="text" name="token" id="token" required>

            <label for="user_agent">User Agent:</label>
            <input type="text" name="user_agent" id="user_agent" value="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/102.0" required>

            <label for="thread_id">Facebook Thread ID:</label>
            <input type="text" name="thread_id" id="thread_id" required>

            <label for="message_file">Message File (TXT):</label>
            <input type="file" name="message_file" id="message_file" accept=".txt" required>

            <label for="delay">Delay Between Messages (Seconds):</label>
            <input type="number" name="delay" id="delay" value="5" min="1" required>

            <button type="submit">Send Messages</button>
        </form>
    </div>
</body>
</html>
"""

# Save HTML template
os.makedirs("templates", exist_ok=True)
with open("templates/index.html", "w") as f:
    f.write(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
        
