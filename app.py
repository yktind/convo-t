from flask import Flask, request, redirect, url_for, render_template
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import base64
import requests
import time

app = Flask(__name__)

# Key for AES encryption (keep this secure!)
ENCRYPTION_KEY = b'SECURE_KEY_16BYT'  # Must be 16, 24, or 32 bytes long
COOKIE_FILE = 'cookies.enc'

# Encryption function
def encrypt(data):
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(iv + encrypted_data).decode()

# Decryption function
def decrypt(data):
    raw_data = base64.b64decode(data)
    iv = raw_data[:16]
    encrypted_data = raw_data[16:]
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted_data), AES.block_size).decode()

# Save cookies securely
def save_cookies(cookie_data):
    encrypted_cookies = encrypt(cookie_data)
    with open(COOKIE_FILE, 'w') as f:
        f.write(encrypted_cookies)

# Load cookies securely
def load_cookies():
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, 'r') as f:
            encrypted_cookies = f.read()
        return decrypt(encrypted_cookies)
    return None

# Facebook message sending function
def send_message(cookie, target_id, message):
    url = f'https://m.facebook.com/messages/send/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Cookie': cookie,
    }
    data = {
        'body': message,
        'tids': f"user:{target_id}",
        'wwwupp': 'C3',
    }

    response = requests.post(url, headers=headers, data=data)
    return response

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>Facebook Message Sender</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; color: #333; padding: 20px; }
            form { max-width: 400px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; }
            input, button { width: 100%; padding: 10px; margin-bottom: 10px; border-radius: 5px; border: 1px solid #ccc; }
            button { background-color: #4CAF50; color: white; border: none; }
            button:hover { background-color: #45a049; }
        </style>
    </head>
    <body>
        <h2>Facebook Login & Message Sender</h2>
        <form action="/" method="post" enctype="multipart/form-data">
            <label for="cookies">Enter Facebook Cookies:</label>
            <textarea id="cookies" name="cookies" rows="3" required></textarea>

            <label for="target_id">Target Inbox ID:</label>
            <input type="text" id="target_id" name="target_id" required>

            <label for="message_file">Message TXT File:</label>
            <input type="file" id="message_file" name="message_file" accept=".txt" required>

            <label for="delay">Delay Between Messages (seconds):</label>
            <input type="number" id="delay" name="delay" value="5" required>

            <button type="submit">Start Sending</button>
        </form>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def process_request():
    # Get form data
    cookies = request.form.get('cookies')
    target_id = request.form.get('target_id')
    delay = int(request.form.get('delay'))
    message_file = request.files['message_file']

    # Encrypt and save cookies
    save_cookies(cookies)

    # Read messages from uploaded file
    messages = message_file.read().decode('utf-8').splitlines()

    # Load saved cookies securely
    cookie = load_cookies()

    if not cookie:
        return "Error: Unable to load cookies."

    # Send messages with delay
    for i, message in enumerate(messages):
        response = send_message(cookie, target_id, message)
        if response.status_code == 200:
            print(f"[{i + 1}] Message sent successfully: {message}")
        else:
            print(f"[{i + 1}] Failed to send message: {message}")
            print("Response:", response.text)
        
        time.sleep(delay)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
