from flask import Flask, request, redirect, url_for, render_template_string
import os
import time
import requests
from bs4 import BeautifulSoup as sop
from concurrent.futures import ThreadPoolExecutor as Executor

app = Flask(__name__)

# Display HTML form for input
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cookie = request.form.get("cookie").strip()
        thread_id = request.form.get("thread_id").strip()
        delay = int(request.form.get("delay", 5))
        messages = request.form.get("messages").splitlines()

        if not authenticate_user(cookie):
            return "Login failed. Check your cookie."

        with Executor(max_workers=5) as executor:
            for message in messages:
                executor.submit(send_message, cookie, thread_id, message.strip(), delay)
        return "Messages sent successfully!"

    # HTML Form
    form_html = '''
    <html>
    <head>
        <title>Facebook Message Automation</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .container { max-width: 600px; margin: auto; padding: 20px; background: #f9f9f9; border-radius: 8px; }
            input, textarea, button { width: 100%; margin-bottom: 10px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
            button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
            button:hover { background-color: #45a049; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Facebook Message Automation</h2>
            <form method="POST">
                <label for="cookie">Facebook Cookie:</label>
                <textarea name="cookie" rows="3" required></textarea>
                
                <label for="thread_id">Thread ID:</label>
                <input type="text" name="thread_id" required>

                <label for="messages">Messages (one per line):</label>
                <textarea name="messages" rows="10" required></textarea>
                
                <label for="delay">Delay Between Messages (seconds):</label>
                <input type="number" name="delay" value="5" min="1" required>
                
                <button type="submit">Send Messages</button>
            </form>
        </div>
    </body>
    </html>
    '''
    return render_template_string(form_html)

# Authenticate the user
def authenticate_user(cookie):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    response = requests.get("https://mbasic.facebook.com", cookies={"cookie": cookie}, headers=headers)
    return "mbasic_logout_button" in response.text

# Send a message to the specified thread
def send_message(cookie, thread_id, message, delay):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    try:
        response = requests.get(
            f"https://mbasic.facebook.com/messages/read/?tid={thread_id}",
            cookies={"cookie": cookie},
            headers=headers
        )
        if response.status_code != 200:
            raise Exception("Failed to load thread.")

        soup = sop(response.text, "html.parser")
        form = soup.find("form", method="post")
        if not form:
            raise Exception("Form not found in response.")

        payload = {inp["name"]: inp["value"] for inp in form.find_all("input") if inp.get("name")}
        payload.update({"body": message, "send": "Send"})

        action_url = form["action"]
        send_response = requests.post(
            f"https://mbasic.facebook.com{action_url}",
            data=payload,
            cookies={"cookie": cookie},
            headers=headers
        )
        if "send" in send_response.url:
            print(f"Message sent: {message}")
        else:
            print(f"Failed to send message: {message}")
        time.sleep(delay)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
