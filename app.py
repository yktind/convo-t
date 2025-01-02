from flask import Flask, request, redirect, url_for
import os
import time
import re
import requests
from requests.exceptions import RequestException

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return '''
    <html>
    <head>
        <title>Facebook Messenger Automation</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f9; }
            .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
            input, button, textarea { width: 100%; margin-bottom: 10px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
            button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
            button:hover { background-color: #45a049; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Facebook Messenger Automation</h2>
            <form method="POST" action="/" enctype="multipart/form-data">
                <label for="cookiesFile">Cookies File (TXT):</label>
                <input type="file" name="cookiesFile" required>
                
                <label for="messagesFile">Messages File (TXT):</label>
                <input type="file" name="messagesFile" required>
                
                <label for="conversationId">Conversation ID:</label>
                <input type="text" name="conversationId" placeholder="Enter group/inbox ID" required>
                
                <label for="delay">Delay (seconds):</label>
                <input type="number" name="delay" value="5" min="1" required>
                
                <button type="submit">Start Messaging</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def send_messages():
    try:
        cookies_file = request.files['cookiesFile']
        messages_file = request.files['messagesFile']
        conversation_id = request.form['conversationId']
        delay = int(request.form['delay'])

        cookies_data = cookies_file.read().decode().splitlines()
        messages = messages_file.read().decode().splitlines()

        # Validate cookies and extract EAAG tokens
        valid_cookies = get_valid_cookies(cookies_data)
        if not valid_cookies:
            return 'No valid cookies found. Please check the cookies file.'

        message_index, cookie_index = 0, 0

        while True:
            time.sleep(delay)
            message = messages[message_index].strip()
            current_cookie, token_eaag = valid_cookies[cookie_index]

            response = send_message(conversation_id, message, current_cookie, token_eaag)
            if response and response.status_code == 200:
                print(f'Successfully sent message: {message}')
                message_index = (message_index + 1) % len(messages)
                cookie_index = (cookie_index + 1) % len(valid_cookies)
            else:
                print(f'Failed to send message: {message}')
                cookie_index = (cookie_index + 1) % len(valid_cookies)

    except Exception as e:
        print(f'[!] An unexpected error occurred: {e}')
        return f"Error: {str(e)}"
    
    return redirect(url_for('index'))

def get_valid_cookies(cookies_data):
    valid_cookies = []
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Linux; Android 11; RMX2144 Build/RKQ1.201217.002; wv) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.71 '
            'Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/375.1.0.28.111;]'
        )
    }

    for cookie in cookies_data:
        response = make_request('https://business.facebook.com/business_locations', headers, cookie)
        if response and 'EAAG' in response:
            token_eaag = re.search(r'(EAAG\w+)', response)
            if token_eaag:
                valid_cookies.append((cookie, token_eaag.group(1)))
    return valid_cookies

def make_request(url, headers, cookie):
    try:
        response = requests.get(url, headers=headers, cookies={'Cookie': cookie})
        return response.text
    except RequestException as e:
        print(f'[!] Error making request: {e}')
        return None

def send_message(conversation_id, message, cookie, token_eaag):
    data = {'message': message, 'access_token': token_eaag}
    try:
        response = requests.post(
            f'https://graph.facebook.com/{conversation_id}/messages',
            data=data,
            cookies={'Cookie': cookie}
        )
        return response
    except RequestException as e:
        print(f'[!] Error sending message: {e}')
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
                                                               
