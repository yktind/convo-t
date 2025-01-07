import os
import time
import requests
from flask import Flask, request, redirect, url_for, render_template_string, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Snap Kit API base URL (conceptual)
SNAPCHAT_OAUTH_URL = 'https://accounts.snapchat.com/oauth2/authorize'
SNAPCHAT_API_URL = 'https://kit.snapchat.com/api/v1'  # This is a placeholder for actual Snap Kit API

# HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Snapchat Messenger</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        textarea, input, button { width: 100%; margin-bottom: 10px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
        button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Snapchat Message Sender</h2>
        {% if not session.get('token') %}
        <p><a href="{{ url_for('login') }}">Login with Snapchat</a></p>
        {% else %}
        <form method="POST" action="{{ url_for('send_message') }}" enctype="multipart/form-data">
            <label for="username">Target Snapchat Username:</label>
            <input type="text" name="username" placeholder="Enter Snapchat username" required>

            <label for="messageFile">Select TXT file with messages:</label>
            <input type="file" name="messageFile" accept=".txt" required>

            <label for="delay">Delay between messages (seconds):</label>
            <input type="number" name="delay" value="5" min="1" required>

            <button type="submit">Send Messages</button>
        </form>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/login')
def login():
    # Construct the URL for Snap Kit OAuth authentication
    return redirect(f"{SNAPCHAT_OAUTH_URL}?client_id=YOUR_SNAP_CLIENT_ID&response_type=code&redirect_uri=http://localhost:5000/callback")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if code:
        # Exchange code for an access token (use OAuth flow)
        token_response = requests.post(
            'https://accounts.snapchat.com/oauth2/access_token',
            data={
                'code': code,
                'client_id': 'YOUR_SNAP_CLIENT_ID',
                'client_secret': 'YOUR_SNAP_CLIENT_SECRET',
                'redirect_uri': 'http://localhost:5000/callback',
                'grant_type': 'authorization_code',
            }
        )
        token_data = token_response.json()
        session['token'] = token_data.get('access_token')  # Store token in session
        return redirect(url_for('index'))
    return "Login failed", 400

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'token' not in session:
        return redirect(url_for('login'))

    # Retrieve form data
    username = request.form['username']
    delay = int(request.form['delay'])
    message_file = request.files['messageFile']
    
    # Read messages from the file
    messages = message_file.read().decode('utf-8').splitlines()

    # Send messages (conceptual example)
    for message in messages:
        send_status = send_snap_message(username, message)
        if send_status:
            print(f"Sent message to {username}: {message}")
        time.sleep(delay)  # Delay between messages

    return "Messages sent successfully!"

def send_snap_message(username, message):
    """Send message to a specific Snapchat user (conceptual)."""
    access_token = session.get('token')
    if access_token:
        response = requests.post(
            f'{SNAPCHAT_API_URL}/messages/send',
            headers={'Authorization': f'Bearer {access_token}'},
            json={'recipient': username, 'message': message}
        )
        return response.status_code == 200
    return False

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    
