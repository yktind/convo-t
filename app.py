from flask import Flask, request, render_template_string, redirect, url_for, flash
import time
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Facebook E2EE Bot (Simulated)</title>
</head>
<body>
  <h2>Facebook Bot Simulation</h2>
  {% with messages = get_flashed_messages() %}
    {% if messages %}
      <ul style="color: green;">
        {% for message in messages %}
          <li>{{ message }}</li>
        {% endfor %}
      </ul>
    {% endif %}
  {% endwith %}
  <form method="POST" action="/send" enctype="multipart/form-data">
    <label>Email:</label><br>
    <input type="email" name="email" required><br><br>

    <label>Password:</label><br>
    <input type="password" name="password" required><br><br>

    <label>Target Chat ID:</label><br>
    <input type="text" name="chat_id" required><br><br>

    <label>Delay (seconds):</label><br>
    <input type="number" name="delay" value="1" min="0"><br><br>

    <label>Select Message File (.txt):</label><br>
    <input type="file" name="message_file" accept=".txt" required><br><br>

    <button type="submit">Start</button>
  </form>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/send', methods=['POST'])
def send():
    email = request.form.get('email')
    password = request.form.get('password')
    chat_id = request.form.get('chat_id')
    delay = int(request.form.get('delay', 1))
    file = request.files['message_file']

    if not all([email, password, chat_id, file]):
        flash("All fields are required!")
        return redirect(url_for('index'))

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    with open(filepath, 'r', encoding='utf-8') as f:
        messages = f.readlines()

    # Simulated sending messages
    for msg in messages:
        msg = msg.strip()
        if msg:
            print(f"Sending to {chat_id}: {msg}")
            time.sleep(delay)

    flash("Messages sent (simulated)!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
  
