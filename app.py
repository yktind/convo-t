from flask import Flask, request, render_template_string
from fbchat import Client
from fbchat.models import *

import time

app = Flask(__name__)

HTML_TEMPLATE = '''
<!doctype html>
<title>Messenger Bot</title>
<h2>Facebook Messenger Automation</h2>
<form method=post>
  Email or Mobile: <input type=text name=email><br><br>
  Password: <input type=password name=password><br><br>
  Target User ID: <input type=text name=target_id><br><br>
  Message: <input type=text name=message><br><br>
  Delay (in seconds): <input type=number name=delay value=2><br><br>
  <input type=submit value=Send>
</form>
<p>{{ status }}</p>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    status = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        target_id = request.form['target_id']
        message = request.form['message']
        delay = int(request.form.get('delay', 2))

        try:
            client = Client(email, password)
            time.sleep(delay)
            client.send(Message(text=message), thread_id=target_id, thread_type=ThreadType.USER)
            client.logout()
            status = "Message sent successfully!"
        except Exception as e:
            status = f"Failed: {e}"

    return render_template_string(HTML_TEMPLATE, status=status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
