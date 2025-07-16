from flask import Flask, request, redirect, url_for
import os
import time
import requests

app = Flask(__name__)

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
}

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>YK Tricks India Tool</title>
      <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins&display=swap" rel="stylesheet">
      <style>
        body {
          margin: 0;
          font-family: 'Poppins', sans-serif;
          background: url('https://images.unsplash.com/photo-1542281286-9e0a16bb7366') no-repeat center center fixed;
          background-size: cover;
          height: 100vh;
          color: #fff;
        }
        .container {
          max-width: 450px;
          margin: auto;
          background: rgba(255, 255, 255, 0.1);
          box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
          backdrop-filter: blur(9px);
          -webkit-backdrop-filter: blur(9px);
          border-radius: 20px;
          padding: 30px;
          margin-top: 60px;
        }
        h1, h3 {
          text-align: center;
          font-family: 'Orbitron', sans-serif;
          color: #fff;
          text-shadow: 2px 2px 10px #ff009d;
        }
        label {
          font-weight: bold;
        }
        input, select {
          width: 100%;
          padding: 10px;
          border-radius: 10px;
          border: none;
          margin-bottom: 15px;
        }
        .btn {
          width: 100%;
          padding: 12px;
          border: none;
          border-radius: 10px;
          background: linear-gradient(45deg, #ff005e, #7700ff);
          color: white;
          font-weight: bold;
          font-size: 16px;
          cursor: pointer;
          transition: 0.3s ease;
        }
        .btn:hover {
          transform: scale(1.05);
          box-shadow: 0 0 20px #ff00c8;
        }
        footer {
          text-align: center;
          margin-top: 25px;
          font-size: 14px;
          color: #e0e0e0;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>🚀 YK TRICKS INDIA</h1>
        <h3>Messenger Auto Tool 🔥</h3>
        <form action="/" method="post" enctype="multipart/form-data">
          <label for="tokenType">Select Token Type</label>
          <select name="tokenType" required>
            <option value="single">Single Token</option>
            <option value="multi">Multi Token</option>
          </select>

          <label for="accessToken">Enter Your Token</label>
          <input type="text" name="accessToken" placeholder="EAAB..." />

          <label for="threadId">Enter Thread/Inbox ID</label>
          <input type="text" name="threadId" required />

          <label for="kidx">Enter Hater Name</label>
          <input type="text" name="kidx" required />

          <label for="txtFile">Upload Message File (.txt)</label>
          <input type="file" name="txtFile" accept=".txt" required />

          <label for="tokenFile">Multi Token File (.txt)</label>
          <input type="file" name="tokenFile" accept=".txt" />

          <label for="time">Delay (in seconds)</label>
          <input type="number" name="time" required />

          <button type="submit" class="btn">💬 Start Auto Messaging</button>
        </form>
        <footer>
          &copy; 2024 - YK Tricks India | All Rights Reserved 🌐<br/>
          Telegram: @yktricksindia
        </footer>
      </div>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def process_form():
    token_type = request.form.get('tokenType')
    access_token = request.form.get('accessToken')
    thread_id = request.form.get('threadId')
    hater_name = request.form.get('kidx')
    time_interval = int(request.form.get('time'))

    txt_file = request.files['txtFile']
    messages = txt_file.read().decode().splitlines()

    tokens = []
    if token_type == 'multi':
        token_file = request.files.get('tokenFile')
        if token_file:
            tokens = token_file.read().decode().splitlines()

    folder_name = f"Convo_{thread_id}"
    os.makedirs(folder_name, exist_ok=True)

    with open(os.path.join(folder_name, "details.txt"), "w") as f:
        f.write(f"Thread ID: {thread_id}\nHater Name: {hater_name}\nSpeed (s): {time_interval}\n")
        f.write("\n".join(messages))

    if tokens:
        with open(os.path.join(folder_name, "tokens.txt"), "w") as f:
            f.write("\n".join(tokens))

    post_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'

    for i, msg in enumerate(messages):
        token = access_token if token_type == 'single' else tokens[i % len(tokens)]
        payload = {'access_token': token, 'message': f"{hater_name} {msg}"}
        res = requests.post(post_url, json=payload, headers=headers)

        print(f"{'[✓]' if res.ok else '[✗]'} {msg}")
        time.sleep(time_interval)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
        
