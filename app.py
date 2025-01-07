import os
import time
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# HTML template for the webpage
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Snapchat Login and Message Sender</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        input, button, textarea { width: 100%; margin-bottom: 10px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
        button { background-color: #FFFC00; color: black; border: none; cursor: pointer; }
        button:hover { background-color: #f2c800; }
        .result { margin-top: 20px; padding: 10px; background-color: #f0f0f0; border-left: 5px solid #FFFC00; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Snapchat Login & Message Automation</h2>
        <form method="POST" action="/" enctype="multipart/form-data">
            <label for="username">Snapchat Username:</label>
            <input type="text" name="username" placeholder="Enter your Snapchat username" required>

            <label for="password">Snapchat Password:</label>
            <input type="password" name="password" placeholder="Enter your Snapchat password" required>

            <label for="messageFile">Message File (TXT):</label>
            <input type="file" name="messageFile" required>

            <label for="delay">Delay (seconds):</label>
            <input type="number" name="delay" value="5" min="1" required>

            <button type="submit">Login and Send Messages</button>
        </form>

        {% if result %}
        <div class="result">
            <strong>Message Sending Status:</strong>
            <p>{{ result }}</p>
        </div>
        {% elif error %}
        <div class="result" style="background-color: #f8d7da; color: #721c24;">
            <strong>Error:</strong>
            <p>{{ error }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

# Mock function to simulate Snapchat login via username/password
def snapchat_login(username, password):
    # Replace with actual Snap Kit OAuth flow for login
    # For educational purposes, mock login:
    if username == "test_user" and password == "test_password":
        return True
    return False

# Simulate sending a message to a Snapchat inbox (this part won't actually send messages)
def send_snapchat_message(username, message, delay=5):
    print(f"Sending message: {message} to {username}")
    time.sleep(delay)
    return f"Message sent: {message}"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        message_file = request.files['messageFile']
        delay = int(request.form['delay'])

        # Check if login is successful
        if not snapchat_login(username, password):
            error = "Login failed. Please check your username and password."
            return render_template_string(HTML_TEMPLATE, result=result, error=error)

        # Read messages from the provided TXT file
        if not message_file:
            error = "Please upload a message file."
            return render_template_string(HTML_TEMPLATE, result=result, error=error)

        messages = message_file.read().decode().splitlines()

        # Simulate sending messages (as Snapchat doesn't allow direct message sending in this way)
        for message in messages:
            result = send_snapchat_message(username, message.strip(), delay)

    return render_template_string(HTML_TEMPLATE, result=result, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
            
