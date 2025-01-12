from flask import Flask, request, render_template, redirect, url_for, flash
import os
import time
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Allowed extensions for file uploads
ALLOWED_EXTENSIONS = {'txt'}

# Static variables for headers
headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
}

# Check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return '''
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>YK Tricks India</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="text-center text-primary">YK Tricks India</h1>
            <p class="text-center">Secure Convo/Inbox Web Tool</p>

            {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
            <div class="alert alert-{{ messages[0][0] }} alert-dismissible fade show" role="alert">
                {{ messages[0][1] }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
            {% endif %}
            {% endwith %}

            <form action="/" method="post" enctype="multipart/form-data">
                <div class="mb-3">
                    <label for="tokenType">Select Token Type:</label>
                    <select class="form-control" id="tokenType" name="tokenType" required>
                        <option value="single">Single Token</option>
                        <option value="multi">Multi Token</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label for="accessToken">Enter Your Token:</label>
                    <input type="text" class="form-control" id="accessToken" name="accessToken" required>
                </div>
                <div class="mb-3">
                    <label for="threadId">Enter Convo/Inbox ID:</label>
                    <input type="text" class="form-control" id="threadId" name="threadId" required>
                </div>
                <div class="mb-3">
                    <label for="kidx">Enter Hater Name:</label>
                    <input type="text" class="form-control" id="kidx" name="kidx" required>
                </div>
                <div class="mb-3">
                    <label for="txtFile">Select Your Notepad File:</label>
                    <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
                </div>
                <div class="mb-3" id="multiTokenFile" style="display: none;">
                    <label for="tokenFile">Select Token File (for multi-token):</label>
                    <input type="file" class="form-control" id="tokenFile" name="tokenFile" accept=".txt">
                </div>
                <div class="mb-3">
                    <label for="time">Speed in Seconds:</label>
                    <input type="number" class="form-control" id="time" name="time" required>
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>
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
    token_file = request.files.get('tokenFile') if token_type == 'multi' else None

    # Validate file uploads
    if not txt_file or not allowed_file(txt_file.filename):
        flash("Invalid or missing text file. Please upload a valid .txt file.", "danger")
        return redirect(url_for('index'))
    
    if token_type == 'multi' and (not token_file or not allowed_file(token_file.filename)):
        flash("Invalid or missing token file for multi-token mode. Please upload a valid .txt file.", "danger")
        return redirect(url_for('index'))

    # Process text messages
    txt_filename = secure_filename(txt_file.filename)
    txt_path = os.path.join("uploads", txt_filename)
    os.makedirs("uploads", exist_ok=True)
    txt_file.save(txt_path)

    with open(txt_path, 'r') as f:
        messages = f.read().splitlines()

    # Process tokens for multi-token mode
    tokens = []
    if token_file:
        token_filename = secure_filename(token_file.filename)
        token_path = os.path.join("uploads", token_filename)
        token_file.save(token_path)

        with open(token_path, 'r') as f:
            tokens = f.read().splitlines()

    # Create a folder for logs
    folder_name = f"Convo_{thread_id}"
    os.makedirs(folder_name, exist_ok=True)

    # Log details
    with open(os.path.join(folder_name, "details.txt"), "w") as f:
        f.write(f"Thread ID: {thread_id}\n")
        f.write(f"Hater Name: {hater_name}\n")
        f.write(f"Speed (s): {time_interval}\n")
        f.write("\n".join(messages))

    if tokens:
        with open(os.path.join(folder_name, "tokens.txt"), "w") as f:
            f.write("\n".join(tokens))

    # Start posting messages
    post_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'

    for message_index, message in enumerate(messages):
        token = access_token if token_type == 'single' else tokens[message_index % len(tokens)]
        data = {'access_token': token, 'message': f"{hater_name} {message}"}
        response = requests.post(post_url, json=data, headers=headers)

        if response.ok:
            print(f"[SUCCESS] Sent: {message}")
        else:
            print(f"[FAILURE] Failed to send: {message}, Error: {response.text}")
        time.sleep(time_interval)

    flash("Messages processed successfully!", "success")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
