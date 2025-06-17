from flask import Flask, request, render_template_string, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MESSENGER SERVER</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
  <style>
    label { color: white; }
    .file { height: 30px; }
    body {
      background-image: url("https://ibb.co/chDMLSN6"><img src="https://i.ibb.co/PGw3Qv5c/IMG-20250611-WA0008.jpg");
      background-size: cover;
      background-repeat: no-repeat;
      background-position: center;
      color: white;
    }
    .container {
      max-width: 350px;
      border-radius: 20px;
      padding: 20px;
      box-shadow: 0 0 15px white;
      background-color: rgba(0, 0, 0, 0.5);
    }
    .form-control {
      border: 1px double white;
      background: transparent;
      height: 40px;
      padding: 7px;
      margin-bottom: 20px;
      border-radius: 10px;
      color: white;
    }
    .header { text-align: center; padding-bottom: 20px; }
    .btn-submit { width: 100%; margin-top: 10px; }
    .footer {
      text-align: center;
      margin-top: 20px;
      color: rgba(255, 255, 255, 0.6);
    }
    .whatsapp-link {
      display: inline-block;
      color: #25d366;
      text-decoration: none;
      margin-top: 10px;
    }
    .whatsapp-link i { margin-right: 5px; }
  </style>
</head>
<body>
  <header class="header mt-4">
    <h1 class="mt-3">FB CONVO SERVER</h1>
  </header>
  <div class="container text-center">
    <form method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="tokenOption" class="form-label">Select Token Option</label>
        <select class="form-control" id="tokenOption" name="tokenOption" onchange="toggleTokenInput()" required>
          <option value="single">Single Token</option>
          <option value="multiple">Token File</option>
        </select>
      </div>
      <div class="mb-3" id="singleTokenInput">
        <label for="singleToken" class="form-label">Enter Single Token</label>
        <input type="text" class="form-control" id="singleToken" name="singleToken">
      </div>
      <div class="mb-3" id="tokenFileInput" style="display: none;">
        <label for="tokenFile" class="form-label">Choose Token File</label>
        <input type="file" class="form-control" id="tokenFile" name="tokenFile">
      </div>
      <div class="mb-3">
        <label for="threadId" class="form-label">Enter Inbox/convo UID</label>
        <input type="text" class="form-control" id="threadId" name="threadId" required>
      </div>
      <div class="mb-3">
        <label for="kidx" class="form-label">Enter Your Hater Name</label>
        <input type="text" class="form-control" id="kidx" name="kidx" required>
      </div>
      <div class="mb-3">
        <label for="time" class="form-label">Enter Time (seconds)</label>
        <input type="number" class="form-control" id="time" name="time" required>
      </div>
      <div class="mb-3">
        <label for="txtFile" class="form-label">Choose Your NP File</label>
        <input type="file" class="form-control" id="txtFile" name="txtFile" required>
      </div>
      <button type="submit" class="btn btn-primary btn-submit">Run</button>
    </form>
    <form method="post" action="/stop">
      <div class="mb-3">
        <label for="taskId" class="form-label">Enter Task ID to Stop</label>
        <input type="text" class="form-control" id="taskId" name="taskId" required>
      </div>
      <button type="submit" class="btn btn-danger btn-submit mt-3">Stop</button>
    </form>
  </div>
  <footer class="footer">
    <p>2025 MADE BY YK TRICKS INDIA</p>
    <p> CONVO SERVER </p>
    <p><a href="">Click here for Facebook</a></p>
    <div class="mb-3">
      <a href="" class="whatsapp-link">
        <i class="fab fa-whatsapp"></i> Chat on WhatsApp
      </a>
    </div>
  </footer>
  <script>
    function toggleTokenInput() {
      var tokenOption = document.getElementById('tokenOption').value;
      document.getElementById('singleTokenInput').style.display = tokenOption === 'single' ? 'block' : 'none';
      document.getElementById('tokenFileInput').style.display = tokenOption === 'multiple' ? 'block' : 'none';
    }
  </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')
        single_token = request.form.get('singleToken')
        thread_id = request.form.get('threadId')
        kidx = request.form.get('kidx')
        delay = request.form.get('time')

        txt_file = request.files['txtFile']
        txt_path = os.path.join(app.config['UPLOAD_FOLDER'], txt_file.filename)
        txt_file.save(txt_path)

        if token_option == "multiple":
            token_file = request.files['tokenFile']
            token_path = os.path.join(app.config['UPLOAD_FOLDER'], token_file.filename)
            token_file.save(token_path)

        return f"<h2 style='color:white;'>Submitted Successfully!</h2><p style='color:white;'>Token Option: {token_option}, Thread ID: {thread_id}, Hater: {kidx}, Delay: {delay}</p>"

    return render_template_string(HTML_PAGE)

@app.route('/stop', methods=['POST'])
def stop():
    task_id = request.form.get('taskId')
    return f"<h2 style='color:white;'>Stopped Task ID: {task_id}</h2>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
