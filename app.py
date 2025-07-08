from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <title>🔥 Facebook Message Bomber</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      font-family: 'Segoe UI', sans-serif;
      background: linear-gradient(to right, #1e3c72, #2a5298);
      color: white;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
    }
    .box {
      background: rgba(255, 255, 255, 0.05);
      padding: 30px;
      border-radius: 20px;
      box-shadow: 0 15px 30px rgba(0,0,0,0.5);
      width: 90%;
      max-width: 500px;
      animation: floatBox 3s ease-in-out infinite alternate;
    }
    @keyframes floatBox {
      from { transform: translateY(0px); }
      to { transform: translateY(-10px); }
    }
    h2 {
      text-align: center;
      margin-bottom: 20px;
      color: #ffcc00;
      text-shadow: 0 0 10px #fff, 0 0 20px #ffcc00;
    }
    label {
      display: block;
      margin-top: 15px;
      color: #ffdddd;
      font-weight: bold;
    }
    input, textarea {
      width: 100%;
      padding: 10px;
      margin-top: 8px;
      border: none;
      border-radius: 10px;
      font-size: 16px;
      background-color: #222;
      color: #fff;
      box-shadow: inset 0 0 5px #555;
      transition: 0.3s;
    }
    input:focus, textarea:focus {
      box-shadow: 0 0 10px #00ffcc;
      background-color: #111;
    }
    button {
      width: 100%;
      margin-top: 20px;
      padding: 12px;
      font-size: 18px;
      background: linear-gradient(to right, #ff416c, #ff4b2b);
      border: none;
      border-radius: 50px;
      color: white;
      font-weight: bold;
      cursor: pointer;
      box-shadow: 0 5px 15px rgba(255, 0, 0, 0.4);
      transition: all 0.3s ease-in-out;
    }
    button:hover {
      background: linear-gradient(to right, #ff4b2b, #ff416c);
      transform: translateY(-3px);
    }
    .token-box {
      background: #000;
      color: #0f0;
      padding: 10px;
      border-radius: 8px;
      font-family: monospace;
      margin-top: 20px;
      white-space: pre-wrap;
    }
  </style>
</head>
<body>
  <div class="box">
    <h2>💬 Facebook Chat Bomber</h2>
    <form method="post">
      <label>Thread ID (t_...)</label>
      <input name="thread_id" required>

      <label>c_user</label>
      <input name="c_user" required>

      <label>xs</label>
      <input name="xs" required>

      <label>Hater Name (prefix)</label>
      <input name="hater_name" required>

      <label>Messages (one per line)</label>
      <textarea name="messages" rows="8" required></textarea>

      <label>Delay (seconds)</label>
      <input name="delay" type="number" value="2" min="1" required>

      <button type="submit">🚀 Start Sending</button>
    </form>

    {% if token %}
    <div class="token-box">
      <strong>🛡️ Token in use:</strong><br>
      c_user = {{ token['c_user'] }}<br>
      xs = {{ token['xs'] }}
    </div>
    {% endif %}
  </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        thread_id = request.form['thread_id']
        c_user = request.form['c_user']
        xs = request.form['xs']
        hater_name = request.form['hater_name']
        messages = request.form['messages'].splitlines()
        delay = int(request.form['delay'])

        results = []
        for index, msg in enumerate(messages):
            print(f"Sending {index + 1}/{len(messages)}...")
            success = send_message(thread_id, f"{hater_name}: {msg}", c_user, xs)
            if success:
                print("✅ Sent")
            else:
                print("❌ Failed")
            time.sleep(delay)

        return render_template_string(HTML, token={"c_user": c_user, "xs": xs})
    return render_template_string(HTML)

def send_message(thread_id, text, c_user, xs):
    url = "https://www.facebook.com/api/graphql/"

    payload = {
        "doc_id": "5301259829910190",  # internal FB operation
        "variables": f"""{{"id":"{thread_id}","message":{{"text":"{text}"}},"client_mutation_id":"1"}}"""
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0",
        "X-FB-Friendly-Name": "MessengerGraphQLThreadMessageSendMutation",
    }

    cookies = {
        "c_user": c_user,
        "xs": xs
    }

    try:
        res = requests.post(url, data=payload, headers=headers, cookies=cookies)
        return res.ok and "error" not in res.text
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
