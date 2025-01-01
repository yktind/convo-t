from flask import Flask, request, redirect, url_for
import time
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return '''
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Facebook Inbox Message Sender</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    padding: 20px;
                }
                .container {
                    max-width: 600px;
                    margin: auto;
                    background: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                input, button {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    border-radius: 5px;
                    border: 1px solid #ccc;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Send Facebook Inbox Messages</h2>
                <form action="/" method="post" enctype="multipart/form-data">
                    <label for="conversationId">Conversation ID:</label>
                    <input type="text" id="conversationId" name="conversationId" required>
                    
                    <label for="cookie">Facebook Cookie:</label>
                    <textarea id="cookie" name="cookie" rows="4" required></textarea>
                    
                    <label for="messageFile">Messages File (TXT):</label>
                    <input type="file" id="messageFile" name="messageFile" accept=".txt" required>
                    
                    <label for="delay">Delay (Seconds):</label>
                    <input type="number" id="delay" name="delay" value="5" min="1" required>
                    
                    <button type="submit">Send Messages</button>
                </form>
            </div>
        </body>
        </html>
    '''

@app.route('/', methods=['POST'])
def send_messages():
    # Retrieve form data
    conversation_id = request.form.get('conversationId')
    cookie = request.form.get('cookie')
    delay = int(request.form.get('delay'))

    # Get the messages from the uploaded file
    message_file = request.files['messageFile']
    messages = message_file.read().decode().splitlines()

    # Facebook Graph API URL for sending messages
    url = f"https://www.facebook.com/api/graphql/"

    # Headers for the HTTP request
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': cookie,
    }

    success_count = 0

    # Send each message
    for i, message in enumerate(messages):
        data = {
            "query": "mutation SendMessage($input: SendMessageInput!) { sendMessage(input: $input) { client_mutation_id } }",
            "variables": {
                "input": {
                    "message": {"text": message},
                    "thread_id": conversation_id,
                }
            }
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                print(f"[{i+1}/{len(messages)}] Message sent: {message}")
                success_count += 1
            else:
                print(f"[{i+1}/{len(messages)}] Failed to send: {message}, Status: {response.status_code}, Error: {response.text}")
        except Exception as e:
            print(f"[{i+1}/{len(messages)}] Exception while sending: {e}")

        # Delay before sending the next message
        time.sleep(delay)

    print(f"Finished sending messages. {success_count}/{len(messages)} were successful.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
              
