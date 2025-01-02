from flask import Flask, request, redirect, url_for
import os
import time
import requests
from requests.exceptions import RequestException

app = Flask(__name__)

# Replace with your Facebook App credentials
APP_ID = 'your_app_id'
APP_SECRET = 'your_app_secret'
ACCESS_TOKEN = 'your_access_token'


@app.route('/', methods=['GET'])
def index():
    return '''
    <html>
    <head>
        <title>Facebook Inbox Message Automation</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 20px; 
                background-color: #f4f4f9; 
            }
            .container { 
                max-width: 800px; 
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
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Facebook Inbox Message Automation</h2>
            <form method="POST" action="/" enctype="multipart/form-data">
                <label for="recipientId">Recipient ID:</label>
                <input type="text" name="recipientId" placeholder="Enter recipient's Facebook ID" required>
                
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


@app.route('/', methods=['POST'])
def send_messages():
    try:
        recipient_id = request.form['recipientId']
        delay = int(request.form['delay'])
        messages_file = request.files['messagesFile']
        messages = messages_file.read().decode().splitlines()

        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }

        for message in messages:
            data = {
                "recipient": {"id": recipient_id},
                "message": {"text": message}
            }

            response = requests.post(
                f'https://graph.facebook.com/v15.0/me/messages',
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                print(f'Successfully sent message: {message}')
            else:
                print(f'Failed to send message: {message}')
                print(f'Response: {response.text}')

            time.sleep(delay)

        return redirect(url_for('index'))

    except RequestException as e:
        print(f'[!] Error: {e}')
        return f"Error: {str(e)}"

    except Exception as e:
        print(f'[!] Unexpected error: {e}')
        return f"Unexpected error: {str(e)}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
        
