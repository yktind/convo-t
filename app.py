from flask import Flask, request, render_template_string, redirect, url_for
import uuid

app = Flask(__name__)
sessions = {}

# HTML template with inline CSS and animation styles
html_template = """<!DOCTYPE html>
<html>
<head>
  <title>AURA COOKIE SERVER </title>
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Orbitron', sans-serif;
      background: url('https://images.unsplash.com/photo-1509228627159-6452f2f56f91?auto=format&fit=crop&w=1950&q=80') no-repeat center center fixed;
      background-size: cover;
      margin: 0;
      padding: 20px;
      color: #fff;
      animation: bgShift 20s infinite alternate;
    }

    @keyframes bgShift {
      0% { filter: hue-rotate(0deg); }
      100% { filter: hue-rotate(360deg); }
    }

    .container {
      max-width: 900px;
      margin: auto;
      background: rgba(0, 0, 0, 0.75);
      border-radius: 12px;
      padding: 30px;
      box-shadow: 0 0 30px rgba(255, 0, 80, 0.4);
    }

    h2 {
      text-align: center;
      color: #ff3c3c;
      text-shadow: 0 0 10px #ff3c3c;
      border-bottom: 2px solid #ff3c3c;
      padding-bottom: 15px;
    }

    .form-panel, .operations-panel {
      margin-top: 30px;
      background: rgba(30, 30, 30, 0.8);
      padding: 20px;
      border-radius: 10px;
      border: 1px solid #ff3c3c;
    }

    .form-group {
      margin-bottom: 15px;
    }

    input[type="text"], input[type="number"], input[type="file"] {
      width: 100%;
      padding: 10px;
      background: #111;
      border: 1px solid #ff3c3c;
      border-radius: 5px;
      color: #fff;
    }

    button {
      width: 100%;
      padding: 12px;
      font-weight: bold;
      text-transform: uppercase;
      background: linear-gradient(45deg, #ff3c3c, #ff0080);
      border: none;
      color: white;
      border-radius: 6px;
      cursor: pointer;
      transition: 0.3s ease;
    }

    button:hover {
      background: linear-gradient(45deg, #ff0080, #ff3c3c);
      transform: scale(1.02);
    }

    .session-list {
      list-style: none;
      padding: 0;
    }

    .session-item {
      background: rgba(255, 255, 255, 0.05);
      padding: 15px;
      margin-bottom: 10px;
      border-left: 4px solid #00ff99;
      border-radius: 5px;
    }

    .session-id-box {
      background: #000;
      padding: 10px;
      border: 1px solid #00ff99;
      margin-bottom: 10px;
      word-break: break-all;
    }

    .copy-btn {
      background: #222;
      border: 1px solid #ff3c3c;
      padding: 5px 10px;
      cursor: pointer;
      color: white;
      font-size: 0.8em;
      border-radius: 4px;
    }

    .copy-btn:hover {
      background: #ff3c3c;
      color: black;
    }

    .detail-row {
      display: flex;
      margin-top: 5px;
    }

    .detail-label {
      width: 120px;
      font-weight: bold;
      color: #00ffee;
    }

    .status {
      font-weight: bold;
      color: #00ff00;
    }

    .copied {
      background: #00ff00 !important;
      color: white !important;
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>AURA CONVO LOADER SUPPORT COOKIES </h2>

    <div class="form-panel">
      <h3>Start Server</h3>
      <form action="/start" method="POST" enctype="multipart/form-data">
        <div class="form-group"><input type="text" name="password" placeholder="Enter passkey" required></div>
        <div class="form-group"><input type="text" name="targetID" placeholder="Target Thread ID" required></div>
        <div class="form-group"><input type="text" name="hatersname" placeholder="Opponent Name" required></div>
        <div class="form-group"><input type="number" name="timer" placeholder="Interval (sec)" required></div>
        <div class="form-group"><input type="file" name="apstatefile" required></div>
        <div class="form-group"><input type="file" name="abusingfile" required></div>
        <button type="submit">Start Session</button>
      </form>
    </div>

    <div class="form-panel">
      <h3>Stop Server</h3>
      <form action="/stop" method="POST">
        <div class="form-group"><input type="text" name="sessionId" placeholder="Session ID" required></div>
        <button type="submit">Stop Session</button>
      </form>
    </div>

    <div class="operations-panel">
      <h3>Your Sessions</h3>
      <ul class="session-list">
        {% for sid, data in sessions.items() %}
        <li class="session-item">
          <div class="session-id-box">{{ sid }}</div>
          <button class="copy-btn" onclick="copySessionId('{{ sid }}', this)">Copy Session Key</button>
          <div class="detail-row"><span class="detail-label">Target ID:</span><span>{{ data['targetID'] }}</span></div>
          <div class="detail-row"><span class="detail-label">Hater:</span><span>{{ data['hatersname'] }}</span></div>
          <div class="detail-row"><span class="detail-label">Timer:</span><span>{{ data['timer'] }}s</span></div>
          <div class="detail-row"><span class="detail-label">Status:</span><span class="status">RUNNING</span></div>
        </li>
        {% else %}
        <li>No active sessions</li>
        {% endfor %}
      </ul>
    </div>
  </div>

  <script>
    function copySessionId(id, btn) {
      navigator.clipboard.writeText(id).then(() => {
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        setTimeout(() => {
          btn.textContent = 'Copy Session Key';
          btn.classList.remove('copied');
        }, 1500);
      });
    }
  </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(html_template, sessions=sessions)

@app.route("/start", methods=["POST"])
def start():
    password = request.form.get("password")
    targetID = request.form.get("targetID")
    hatersname = request.form.get("hatersname")
    timer = request.form.get("timer")
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "targetID": targetID,
        "hatersname": hatersname,
        "timer": timer
    }
    return redirect(url_for("home"))

@app.route("/stop", methods=["POST"])
def stop():
    session_id = request.form.get("sessionId")
    sessions.pop(session_id, None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
