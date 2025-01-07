from flask import Flask, request, render_template_string, redirect, url_for
import time
import requests

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Snapchat Messenger</title>
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
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Snapchat Automated Messenger</h2>
        <form method="POST" action="/" enctype="multipart/form-data">
            <label for="username">Snapchat Username:</label>
            <input type="text" name="username" placeholder="Your Snapchat username" required>
            
            <label for="password">Snapchat Password:</label>
            <input type="password" name="password" placeholder="Your Snapchat password" required>
            
            <label for="target">Target Snapchat Username:</label>
            <input type="text" name="target" placeholder="Target Snapchat username" required>
            
            <label for="messagesFile">Messages File (TXT):</label>
            <input type="file" name="messagesFile" required>
            
            <label for="delay">Delay (seconds):</label>
            <input type="number" name="delay" value="5" min="1" required>
            
            <button type="submit">Start Sending Messages</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        target = request.form['target']
        delay = int(request.form['delay'])
        messages_file = request.files['messagesFile']
        
        messages = messages_file.read().decode().splitlines()
        if not login_to_snapchat(username, password):
            return render_template_string(HTML_TEMPLATE + '<p class="error">Login failed. Check your credentials.</p>')
        
        for message in messages:
            send_message(target, message)
            time.sleep(delay)
        
        return render_template_string(HTML_TEMPLATE + '<p>Messages sent successfully!</p>')
    return render_template_string(HTML_TEMPLATE)

def login_to_snapchat(username, password):
    # Mocking a Snapchat login API request (replace with actual API logic)
    print(f"Logging in with username: {username}")
    if username == "testuser" and password == "testpass":  # Replace with actual validation
        return True
    return False

def send_message(target, message):
    # Mocking a Snapchat send message API request (replace with actual API logic)
    print(f"Sending message to {target}: {message}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
