import os
import requests
import time
from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# HTML Template for the Flask Web Page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Facebook Messenger Automation</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 0; }
        .container { max-width: 600px; margin: 50px auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        input, button, textarea { width: 100%; margin-bottom: 15px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
        button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
        .stop-button { background-color: #ff4d4d; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Facebook Messenger Automation</h2>
        <form method="POST" action="/" enctype="multipart/form-data">
            <label for="token">Enter Facebook Token (EAAB...):</label>
            <input type="text" name="token" placeholder="Enter your access token" required>
            
            <label for="recipient">Recipient ID (Inbox/Group Chat):</label>
            <input type="text" name="recipient" placeholder="Enter recipient ID" required>
            
            <label for="messagesFile">Upload Messages File (TXT):</label>
            <input type="file" name="messagesFile" required>
            
            <label for="delay">Delay (seconds):</label>
            <input type="number" name="delay" value="5" min="1" required>
            
            <button type="submit">Start Messaging</button>
        </form>
        <form method="POST" action="/stop">
            <button type="submit" class="stop-button">Stop Messaging</button>
        </form>
    </div>
</body>
</html>
'''

# Global variable to manage the messaging process
STOP_PROCESS = False

@app.route('/', methods=['GET', 'POST'])
def index():
    global STOP_PROCESS
    if request.method == 'POST':
        STOP_PROCESS = False
        token = request.form['token']
        recipient = request.form['recipient']
        delay = int(request.form['delay'])
        messages_file = request.files['messagesFile']
        
        if not token or not recipient or not messages_file:
            return "Error: All fields are required."
        
        messages = messages_file.read().decode().splitlines()
        for message in messages:
            if STOP_PROCESS:
                break
            send_message(token, recipient, message.strip())
            time.sleep(delay)
        
        return "Messages sent successfully!" if not STOP_PROCESS else "Messaging stopped by user."
    
    return render_template_string(HTML_TEMPLATE)

@app.route('/stop', methods=['POST'])
def stop():
    global STOP_PROCESS
    STOP_PROCESS = True
    return "Messaging process stopped."

def send_message(token, recipient_id, message):
    """Send a message using the Facebook Graph API."""
    url = f"https://graph.facebook.com/v15.0/{recipient_id}/messages"
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'recipient': {'id': recipient_id}, 'message': {'text': message}}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"[✔] Message sent: {message}")
        else:
            print(f"[✘] Failed to send message: {response.json()}")
    except Exception as e:
        print(f"[✘] Error: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
