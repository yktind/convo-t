from flask import Flask, request, render_template, jsonify
import requests
import os
import time
from threading import Thread

app = Flask(__name__)
app.secret_key = "supersecretkey"

# User-Agent header for Facebook requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
}


def extract_token(cookies):
    """Extract EAAB access token from Facebook cookies."""
    try:
        response = requests.get("https://graph.facebook.com/v17.0/me", cookies={"cookie": cookies}, headers=HEADERS)
        if response.status_code == 200:
            token = response.json().get("access_token")
            if token and token.startswith("EAAB"):
                return token
        return None
    except Exception as e:
        print(f"Error extracting token: {e}")
        return None


def send_message(token, thread_id, messages, delay):
    """Send messages to a Facebook inbox/chat."""
    for message in messages:
        try:
            payload = {
                "message": message.strip(),
                "recipient": {"id": thread_id},
            }
            response = requests.post(
                f"https://graph.facebook.com/v17.0/me/messages?access_token={token}",
                json=payload,
                headers=HEADERS,
            )
            if response.status_code == 200:
                print(f"Message sent: {message.strip()}")
            else:
                print(f"Failed to send message: {message.strip()} - {response.text}")
            time.sleep(delay)
        except Exception as e:
            print(f"Error sending message: {e}")
            break


@app.route("/")
def index():
    """Render the main page."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Facebook Message Sender</title>
    </head>
    <body>
        <h1>Facebook Message Sender</h1>
        <form action="/submit" method="POST" enctype="multipart/form-data">
            <label for="cookies">Enter Facebook Cookies:</label><br>
            <textarea id="cookies" name="cookies" rows="4" cols="50" required></textarea><br><br>
            
            <label for="thread_id">Enter Thread/Recipient ID:</label><br>
            <input type="text" id="thread_id" name="thread_id" required><br><br>
            
            <label for="delay">Enter Delay (in seconds):</label><br>
            <input type="number" id="delay" name="delay" min="1" value="5" required><br><br>
            
            <label for="message_file">Upload Message File (TXT):</label><br>
            <input type="file" id="message_file" name="message_file" accept=".txt" required><br><br>
            
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    """


@app.route("/submit", methods=["POST"])
def submit():
    """Handle form submission."""
    try:
        # Get cookies, thread ID, and delay
        cookies = request.form.get("cookies")
        thread_id = request.form.get("thread_id")
        delay = int(request.form.get("delay"))
        message_file = request.files.get("message_file")

        # Validate input
        if not cookies or not thread_id or not message_file:
            return "Missing required fields.", 400

        # Save and read the message file
        messages = message_file.read().decode("utf-8").splitlines()

        # Extract token
        token = extract_token(cookies)
        if not token:
            return "Failed to extract token. Please check your cookies.", 400

        # Start sending messages in a separate thread
        Thread(target=send_message, args=(token, thread_id, messages, delay)).start()

        return "Messages are being sent in the background. Check the logs for updates."
    except Exception as e:
        return f"Error: {e}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
        
