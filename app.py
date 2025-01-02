from flask import Flask, request, jsonify, redirect, url_for
import os
import re
import time
import requests
from bs4 import BeautifulSoup as sop
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=10)  # Limit parallel tasks

def authenticate_cookie(cookie):
    """Validate Facebook cookie."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'
    }
    response = requests.get("https://mbasic.facebook.com", cookies={"cookie": cookie}, headers=headers)
    if "mbasic_logout_button" in response.text:
        return True
    return False

def send_message(cookie, thread_id, message):
    """Send a message to a Facebook thread."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    try:
        session = requests.Session()
        # Access the thread
        thread_url = f"https://mbasic.facebook.com/messages/read/?tid={thread_id}"
        response = session.get(thread_url, cookies={"cookie": cookie}, headers=headers)
        if response.status_code != 200:
            raise Exception("Failed to access thread.")
        
        # Parse form details for message posting
        soup = sop(response.text, "html.parser")
        form = soup.find("form", method="post")
        if not form:
            raise Exception("Unable to locate the message form.")

        # Collect required form data
        payload = {inp["name"]: inp["value"] for inp in form.find_all("input") if inp.get("name")}
        payload["body"] = message
        payload["send"] = "Send"

        # Send message
        action_url = form["action"]
        send_response = session.post(f"https://mbasic.facebook.com{action_url}", data=payload, headers=headers)
        if "send" not in send_response.url:
            raise Exception("Message failed.")
        
        return {"status": "success", "message": message}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/', methods=['GET'])
def index():
    """Return the main page."""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Facebook Messenger Automation</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f4f4f9; margin: 0; padding: 0; }
            .container { max-width: 800px; margin: 50px auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
            input, textarea, button { display: block; width: 100%; margin-bottom: 10px; padding: 10px; border-radius: 5px; border: 1px solid #ccc; }
            button { background: #4CAF50; color: white; border: none; cursor: pointer; }
            button:hover { background: #45a049; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Facebook Messenger Automation</h2>
            <form method="POST" action="/send-messages">
                <label for="cookie">Facebook Cookie:</label>
                <input type="text" id="cookie" name="cookie" placeholder="Enter your Facebook cookie" required>
                
                <label for="thread_id">Thread ID:</label>
                <input type="text" id="thread_id" name="thread_id" placeholder="Enter the thread ID" required>
                
                <label for="message">Message:</label>
                <textarea id="message" name="message" placeholder="Enter your message" required></textarea>
                
                <label for="delay">Delay (seconds):</label>
                <input type="number" id="delay" name="delay" min="1" value="5" required>
                
                <button type="submit">Start Sending Messages</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/send-messages', methods=['POST'])
def send_messages():
    """Handle message-sending requests."""
    try:
        cookie = request.form["cookie"].strip()
        thread_id = request.form["thread_id"].strip()
        message = request.form["message"].strip()
        delay = int(request.form["delay"])

        if not authenticate_cookie(cookie):
            return "Invalid Facebook Cookie. Please check and try again."

        def message_worker():
            for i in range(1, 6):  # Example loop: sends 5 messages
                time.sleep(delay)
                result = send_message(cookie, thread_id, f"{message} ({i})")
                print(result)  # Log output for debugging

        executor.submit(message_worker)
        return "Message-sending process started in the background. Check the console for progress."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
        
