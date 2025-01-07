from flask import Flask, request, render_template_string
import os
import time
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import requests

app = Flask(__name__)

# HTML template for the Flask app
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Encrypted Messenger</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        textarea, input, button {
            width: 100%;
            margin-bottom: 10px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            padding: 10px;
            background-color: #f0f0f0;
            border-left: 5px solid #4CAF50;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
            border-left: 5px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Facebook Encrypted Messenger</h2>
        <form method="POST" action="/">
            <label for="token">Access Token:</label>
            <textarea name="token" rows="2" placeholder="Enter your Facebook access token..." required></textarea>
            
            <label for="page_id">Page ID:</label>
            <input type="text" name="page_id" placeholder="Enter your Page ID" required>
            
            <label for="recipient_id">Recipient ID:</label>
            <input type="text" name="recipient_id" placeholder="Enter the Recipient ID" required>
            
            <label for="messages">Messages (one per line):</label>
            <textarea name="messages" rows="5" placeholder="Enter messages, one per line..." required></textarea>
            
            <label for="delay">Delay (seconds):</label>
            <input type="number" name="delay" value="5" min="1" required>
            
            <button type="submit">Send Encrypted Messages</button>
        </form>
        {% if result %}
        <div class="result">
            <strong>Result:</strong>
            <p>{{ result }}</p>
        </div>
        {% elif error %}
        <div class="result error">
            <strong>Error:</strong>
            <p>{{ error }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

# Encryption Functions
def generate_key():
    """Generate a random AES key."""
    return get_random_bytes(16)  # AES-128 key

def encrypt_message(key, message):
    """Encrypt a message using AES in CBC mode."""
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv, base64.b64encode(ct_bytes).decode()

# Facebook Message Sending
def send_message(access_token, page_id, recipient_id, encrypted_message, iv):
    """Send encrypted message via Facebook Messenger."""
    url = f"https://graph.facebook.com/v15.0/{page_id}/messages"
    headers = {'Authorization': f'Bearer {access_token}'}
    iv_base64 = base64.b64encode(iv).decode()
    
    payload = {
        'recipient': {'id': recipient_id},
        'message': {
            'text': f"Encrypted Message:\nIV: {iv_base64}\nMessage: {encrypted_message}"
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return f"Message sent successfully: {encrypted_message}"
        else:
            return f"Failed to send message: {response.json()}"
    except Exception as e:
        return f"Error: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        try:
            access_token = request.form['token']
            page_id = request.form['page_id']
            recipient_id = request.form['recipient_id']
            messages = request.form['messages'].strip().split('\n')
            delay = int(request.form['delay'])
            
            key = generate_key()
            results = []
            
            for message in messages:
                iv, encrypted_message = encrypt_message(key, message)
                result = send_message(access_token, page_id, recipient_id, encrypted_message, iv)
                results.append(result)
                time.sleep(delay)
            
            result = "\n".join(results)
        except Exception as e:
            error = f"An error occurred: {e}"
    
    return render_template_string(HTML_TEMPLATE, result=result, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
            
