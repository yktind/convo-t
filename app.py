from flask import Flask, request, redirect, url_for, jsonify
import os
import time
import re
import requests
from requests.exceptions import RequestException
import threading

app = Flask(__name__)

stop_flag = False

@app.route('/', methods=['GET'])
def index():
    return '''
    <html>
    <head>
        <title>🔥 VIP Facebook Commenter</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Bungee&display=swap" rel="stylesheet">
        <style>
            html, body {
                margin: 0;
                padding: 0;
                height: 100%;
                width: 100%;
                font-family: 'Bungee', cursive;
                background-color: #000000;
                color: #ff0066;
                overflow-x: hidden;
            }
            .container {
                width: 95%;
                max-width: 450px;
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                background: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(10px);
                padding: 30px 20px;
                border-radius: 20px;
                box-shadow: 0 0 30px #ff0077, 0 0 10px #ff3399 inset;
                border: 2px solid #ff3399;
                margin: auto;
            }
            h2 {
                text-align: center;
                font-size: 20px;
                margin-bottom: 30px;
                color: #ffffff;
                text-shadow: 0 0 12px #ff3399;
            }
            input, button, textarea {
                width: 100%;
                margin-bottom: 16px;
                padding: 12px;
                border: none;
                border-radius: 10px;
                font-size: 12px;
                background: #ffe6f0;
                color: #990033;
                box-shadow: inset 0 0 6px #ff3399;
                transition: 0.3s ease;
                font-family: 'Bungee', cursive;
            }
            input:focus, textarea:focus {
                outline: none;
                box-shadow: 0 0 12px #ff3399;
                transform: scale(1.01);
            }
            button {
                background: linear-gradient(90deg, #ff0066, #cc0066);
                color: #ffffff;
                font-weight: bold;
                cursor: pointer;
                transition: 0.3s ease;
                box-shadow: 0 0 15px #ff3399;
            }
            button:hover {
                transform: scale(1.03);
                background: linear-gradient(90deg, #ff3399, #cc0066);
                box-shadow: 0 0 22px #ff3399;
            }
            label {
                font-weight: bold;
                margin-bottom: 6px;
                display: block;
                color: #ffffff;
                font-size: 12px;
                text-shadow: 0 0 5px #ff3399;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🔥 VIP Facebook Comment Automation</h2>
            <form method="POST" action="/" enctype="multipart/form-data">
                <label for="cookiesFile">📜 Cookies File (TXT):</label>
                <input type="file" name="cookiesFile" required>

                <label for="commentsFile">🗒️ Comments File (TXT):</label>
                <input type="file" name="commentsFile" required>

                <label for="commenterName">👤 Commenter's Name:</label>
                <input type="text" name="commenterName" placeholder="Enter name..." required>

                <label for="postId">🧾 Facebook Post ID:</label>
                <input type="text" name="postId" placeholder="Enter post ID..." required>

                <label for="delay">⏱️ Delay (seconds):</label>
                <input type="number" name="delay" value="5" min="1" required>

                <button type="submit">🚀 Start Commenting</button>
            </form>
            <button onclick="stopBot()" style="background: linear-gradient(90deg,#ff0000,#990000);">🚫 Stop Commenting</button>
        </div>
        <script>
            function stopBot() {
                fetch('/stop', { method: 'POST' })
                .then(res => res.json())
                .then(data => alert(data.message))
                .catch(err => alert('Error stopping bot.'));
            }
        </script>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def send_comments():
    global stop_flag
    stop_flag = False

    def run_bot():
        try:
            cookies_file = request.files['cookiesFile']
            comments_file = request.files['commentsFile']
            commenter_name = request.form['commenterName']
            post_id = request.form['postId']
            delay = int(request.form['delay'])

            cookies_data = cookies_file.read().decode().splitlines()
            comments = comments_file.read().decode().splitlines()

            valid_cookies = get_valid_cookies(cookies_data)
            if not valid_cookies:
                return 'No valid cookies found. Please check the cookies file.'

            x, cookie_index = 0, 0

            while not stop_flag:
                time.sleep(delay)
                comment = comments[x].strip()
                current_cookie, token_eaag = valid_cookies[cookie_index]

                response = post_comment(post_id, commenter_name, comment, current_cookie, token_eaag)
                if response and response.status_code == 200:
                    print(f'Successfully sent comment: {commenter_name}: {comment}')
                    x = (x + 1) % len(comments)
                    cookie_index = (cookie_index + 1) % len(valid_cookies)
                else:
                    print(f'Failed to send comment: {commenter_name}: {comment}')
                    cookie_index = (cookie_index + 1) % len(valid_cookies)
        except Exception as e:
            print(f'[!] An unexpected error occurred: {e}')

    thread = threading.Thread(target=run_bot)
    thread.start()
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop():
    global stop_flag
    stop_flag = True
    return jsonify({'message': '✅ Comment bot stopped successfully!'})

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

def post_comment(post_id, commenter_name, comment, cookie, token_eaag):
    data = {'message': f'{commenter_name}: {comment}', 'access_token': token_eaag}
    try:
        response = requests.post(
            f'https://graph.facebook.com/{post_id}/comments/',
            data=data,
            cookies={'Cookie': cookie}
        )
        return response
    except RequestException as e:
        print(f'[!] Error posting comment: {e}')
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
