from flask import Flask, request, render_template, redirect, url_for, flash
import os
import time
import requests
from werkzeug.utils import secure_filename
from Crypto.Cipher import AES
import base64
import hashlib

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

# Encrypt a message using AES (CBC mode with random IV)
def encrypt_message(message, key):
    key = hashlib.sha256(key.encode()).digest()  # Use a SHA-256 hash of the key as AES requires a 32-byte key
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    message = message.encode('utf-8')
    padding = 16 - len(message) % 16
    message += bytes([padding]) * padding  # Apply PKCS7 padding
    encrypted = cipher.encrypt(message)
    return base64.b64encode(iv + encrypted).decode('utf-8')

@app.route('/')
def index():
    return '''
        <div id='content'>
<!-- info --><div style="font-size: 20px">
<script type="text/javascript">
farbbibliothek = new Array();
farbbibliothek[0] = new Array("#FF0000","#FF1100","#FF2200","#FF3300","#FF4400","#FF5500","#FF6600","#FF7700","#FF8800","#FF9900","#FFaa00","#FFbb00","#FFcc00","#FFdd00","#FFee00","#FFff00","#FFee00","#FFdd00","#FFcc00","#FFbb00","#FFaa00","#FF9900","#FF8800","#FF7700","#FF6600","#FF5500","#FF4400","#FF3300","#FF2200","#FF1100");
farbbibliothek[1] = new Array("#00FF00","#000000","#00FF00","#00FF00");
farbbibliothek[2] = new Array("#00FF00","#FF0000","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00","#00FF00");
farbbibliothek[3] = new Array("#FF0000","#FF4000","#FF8000","#FFC000","#FFFF00","#C0FF00","#80FF00","#40FF00","#00FF00","#00FF40","#00FF80","#00FFC0","#00FFFF","#00C0FF","#0080FF","#0040FF","#0000FF","#4000FF","#8000FF","#C000FF","#FF00FF","#FF00C0","#FF0080","#FF0040");
farbbibliothek[4] = new Array("#FF0000","#EE0000","#DD0000","#CC0000","#BB0000","#AA0000","#990000","#880000","#770000","#660000","#550000","#440000","#330000","#220000","#110000","#000000","#110000","#220000","#330000","#440000","#550000","#660000","#770000","#880000","#990000","#AA0000","#BB0000","#CC0000","#DD0000","#EE0000");
farbbibliothek[5] = new Array("#000000","#000000","#000000","#FFFFFF","#FFFFFF","#FFFFFF");
farbbibliothek[6] = new Array("#0000FF","#FFFF00");
farben = farbbibliothek[4];
function farbschrift(){for(var b=0;b<Buchstabe.length;b++){document.all["a"+b].style.color=farben[b]}farbverlauf()}function string2array(b){Buchstabe=new Array();while(farben.length<b.length){farben=farben.concat(farben)}k=0;while(k<=b.length){Buchstabe[k]=b.charAt(k);k++}}function divserzeugen(){for(var b=0;b<Buchstabe.length;b++){document.write("<span id='a"+b+"' class='a"+b+"'>"+Buchstabe[b]+"</span>")}farbschrift()}var a=1;function farbverlauf(){for(var b=0;b<farben.length;b++){farben[b-1]=farben[b]}farben[farben.length-1]=farben[-1];setTimeout("farbschrift()",30)}var farbsatz=1;function farbtauscher(){farben=farbbibliothek[farbsatz];while(farben.length<text.length){farben=farben.concat(farben)}farbsatz=Math.floor(Math.random()*(farbbibliothek.length-0.0001))}setInterval("farbtauscher()",5000);
 
text= "ðŸ’™ðŸ’šâ¤ï¸THIS WEB PAGE IS MADE BY Mr.YK TRICKS INDIA ðŸ’«ðŸ’¯ðŸŸ¥ðŸŸ¨ðŸŸ§OWNER :- Mr.YK TRICKS INDIA âœ¨ðŸðŸŒ¹"; //h
string2array(text);
divserzeugen();
//document.write(text);
</script></div>
<p id='name'>           
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>YK Tricks India</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #f0f8ff;
                animation: colorCycle 5s infinite linear;
            }
            @keyframes colorCycle {
                0% { background-color: #f0f8ff; }
                25% { background-color: #ffebcd; }
                50% { background-color: #98fb98; }
                75% { background-color: #e0ffff; }
                100% { background-color: #f0f8ff; }
            }
            .text-color-animation {
                animation: textColorCycle 3s infinite linear;
            }
            @keyframes textColorCycle {
                0% { color: #FF6347; }
                25% { color: #4682B4; }
                50% { color: #32CD32; }
                75% { color: #FFD700; }
                100% { color: #FF6347; }
            }
            .container {
                max-width: 500px;
                background-color: #fff;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                margin: 20px auto;
            }
            .header {
                text-align: center;
                padding-bottom: 10px;
            }
            .btn-submit {
                width: 100%;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="text-center text-primary text-color-animation">YK Tricks India</h1>
            <p class="text-center">Secure Convo/Inbox Web Tool</p>

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
                    <label for="chatType">Select Chat Type:</label>
                    <select class="form-control" id="chatType" name="chatType" required>
                        <option value="inbox">Inbox</option>
                        <option value="group">Group Chat</option>
                        <option value="encrypted">Encrypted</option>
                    </select>
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
    chat_type = request.form.get('chatType')  # Added chat type selection

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

    # Start posting messages based on selected chat type
    post_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'

    for message_index, message in enumerate(messages):
        token = access_token if token_type == 'single' else tokens[message_index % len(tokens)]
        
        if chat_type == 'encrypted':  # Encrypt the message for end-to-end encryption
            encrypted_message = encrypt_message(message, access_token)  # Use access_token as the encryption key
            data = {'access_token': token, 'message': encrypted_message}
        else:
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
    
