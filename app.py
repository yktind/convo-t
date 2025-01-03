from flask import Flask, request
import requests
import time
import threading

app = Flask(__name__)

# To manage the state of the automation thread
running = False

def send_messages(cookie, txt_file, target_id, delay):
    """
    Send messages to a Facebook target using the provided cookie, message file, and delay.
    """
    global running
    running = True

    # Facebook message endpoint
    fb_message_url = f"https://www.facebook.com/messages/t/{target_id}"

    # Load messages from the text file
    with open(txt_file, 'r') as file:
        messages = file.readlines()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": cookie
    }

    session = requests.Session()
    session.headers.update(headers)

    for message in messages:
        if not running:
            break

        data = {
            "body": message.strip(),
            "action_type": "ma-type:user-generated-message",
        }

        # Sending the message
        response = session.post(fb_message_url, data=data)

        if response.status_code == 200:
            print(f"Message sent: {message.strip()}")
        else:
            print(f"Failed to send message: {message.strip()} | Status: {response.status_code}")

        time.sleep(delay)

def stop_automation():
    """
    Stop the running automation process.
    """
    global running
    running = False

@app.route('/start', methods=['POST'])
def start():
    """
    Start the automation process.
    """
    global running
    if running:
        return "Automation is already running!"

    cookie = request.form['cookie']
    txt_file = request.form['txt_file']
    target_id = request.form['target_id']
    delay = int(request.form['delay'])

    automation_thread = threading.Thread(target=send_messages, args=(cookie, txt_file, target_id, delay))
    automation_thread.start()

    return "Automation started successfully!"

@app.route('/stop', methods=['POST'])
def stop():
    """
    Stop the automation process.
    """
    stop_automation()
    return "Automation stopped successfully!"

@app.route('/')
def home():
    """
    Simple response for the root route.
    """
    return """
    <h1>Facebook Automation</h1>
    <form action="/start" method="post">
        <label>Cookie:</label><br>
        <input type="text" name="cookie" required><br><br>
        <label>Message File (Path):</label><br>
        <input type="text" name="txt_file" required><br><br>
        <label>Target User ID:</label><br>
        <input type="text" name="target_id" required><br><br>
        <label>Delay (Seconds):</label><br>
        <input type="number" name="delay" required><br><br>
        <button type="submit">Start Automation</button>
    </form>
    <br>
    <form action="/stop" method="post">
        <button type="submit">Stop Automation</button>
    </form>
    """

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    
