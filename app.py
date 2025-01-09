from flask import Flask, request, render_template_string, redirect, url_for
import time
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os

app = Flask(__name__)

# Encryption key for securing the token
ENCRYPTION_KEY = b"mysecretkey12345"  # Must be 16, 24, or 32 bytes

# HTML template for the web page
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
            background-color: #f4f4f9;
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
        input, button, textarea {
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
        .error {
            color: red;
            margin-top: 10px;
        }
        .success {
            color: green;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Facebook Page Messenger</h2>
        <form method="POST" action="/" enctype="multipart/form-data">
            <label for="token">Facebook Token:</label>
            <input type="text" name="token" placeholder="Enter your Facebook token" required>

            <label for="page_id">Page ID:</label>
            <input type="text" name="page_id" placeholder="Enter the Facebook Page ID" required>

            <label for="message_file">Message File (TXT):</label>
            <input type="file" name="message_file" required>

            <label for="delay">Delay (seconds):</label>
            <input type="number" name="delay" value="5" min="1" required>

            <button type="submit">Start Sending</button>
        </form>

        {% if error %}
        <p class="error">{{ error }}</p>
        {% elif success %}
        <p class="success">{{ success }}</p>
        {% endif %}
    </div>
</body>
</html>
'''

# Helper function to encrypt data
def encrypt(data):
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC)
    iv = cipher.iv
    encrypted = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(iv + encrypted).decode()

# Helper function to decrypt data
def decrypt(data):
    raw = base64.b64decode(data)
    iv = raw[:16]
    encrypted = raw[16:]
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted), AES.block_size).decode()

# Function to send a message to the Facebook page
def send_message(token, page_id, message):
    url = f"https://graph.facebook.com/{page_id}/feed"
    data = {"message": message, "access_token": token}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Error sending message: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            token = request.form['token']
            page_id = request.form['page_id']
            delay = int(request.form['delay'])
            message_file = request.files['message_file']

            # Encrypt the token for added security
            encrypted_token = encrypt(token)

            # Read messages from the file
            messages = message_file.read().decode().splitlines()

            # Send messages with a delay
            for message in messages:
                success = send_message(decrypt(encrypted_token), page_id, message)
                if success:
                    print(f"Message sent: {message}")
                else:
                    return render_template_string(
                        HTML_TEMPLATE, error="Failed to send some messages. Check your token and page ID."
                    )
                time.sleep(delay)

            return render_template_string(HTML_TEMPLATE, success="All messages sent successfully!")
        except Exception as e:
            print(f"Error: {e}")
            return render_template_string(HTML_TEMPLATE, error="An unexpected error occurred.")
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
                          
