from flask import Flask, request, render_template_string, redirect, url_for
import time
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os

app = Flask(__name__)

# Encryption key (you should generate and keep it secure)
SECRET_KEY = os.urandom(16)

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Page Messenger</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
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
    </style>
</head>
<body>
    <div class="container">
        <h2>Facebook Page Messenger</h2>
        <form method="POST" action="/" enctype="multipart/form-data">
            <label for="token">Facebook Access Token:</label>
            <input type="text" name="token" placeholder="Enter your Facebook token" required>

            <label for="page_id">Facebook Page ID:</label>
            <input type="text" name="page_id" placeholder="Enter the page ID" required>

            <label for="message_file">Message File (TXT):</label>
            <input type="file" name="message_file" required>

            <label for="delay">Delay (seconds):</label>
            <input type="number" name="delay" value="5" min="1" required>

            <button type="submit">Start Sending Messages</button>
        </form>
        {% if result %}
        <div class="result">
            <h4>Result:</h4>
            <p>{{ result }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

# Encrypt token
def encrypt_token(token):
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_token = cipher.encrypt(pad(token.encode(), AES.block_size))
    return base64.b64encode(iv + encrypted_token).decode()

# Decrypt token
def decrypt_token(encrypted_token):
    raw = base64.b64decode(encrypted_token)
    iv = raw[:16]
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    decrypted_token = unpad(cipher.decrypt(raw[16:]), AES.block_size)
    return decrypted_token.decode()

# Send messages to the page
def send_message(page_id, token, message):
    url = f"https://graph.facebook.com/{page_id}/feed"
    data = {
        "message": message,
        "access_token": token
    }
    response = requests.post(url, data=data)
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        token = request.form['token']
        page_id = request.form['page_id']
        delay = int(request.form['delay'])
        message_file = request.files['message_file']

        # Encrypt token
        encrypted_token = encrypt_token(token)

        # Read messages from the uploaded file
        messages = message_file.read().decode().splitlines()

        # Send messages with delay
        try:
            for message in messages:
                response = send_message(page_id, decrypt_token(encrypted_token), message)
                if response.status_code == 200:
                    print(f"Message sent: {message}")
                else:
                    print(f"Failed to send message: {response.text}")
                time.sleep(delay)
            result = "Messages sent successfully!"
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
                
