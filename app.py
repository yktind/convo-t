from flask import Flask, request, render_template_string

app = Flask(__name__)

# Your full HTML page as a Python multiline string (use triple quotes)
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Facebook Message Automation Using Cookies</title>
  <style>
        /* Your full CSS here as provided */
        body, html {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
            color: #333;
        }

        header {
            position: relative;
            width: 100%;
            height: 120px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }

        .header-wrapper {
            display: flex;
            width: 100%;
            height: 100%;
            position: relative;
        }

        .header-left {
            flex: 1;
            background: #7d7dff;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Arial Black', sans-serif;
            font-style: italic;
            clip-path: polygon(0 0, 100% 0, 90% 100%, 0% 100%);
        }

        .header-right {
            flex: 1;
            background: white;
            color: black;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Arial Black', sans-serif;
            font-style: italic;
            clip-path: polygon(10% 0, 100% 0, 100% 100%, 0 100%);
        }

        .header-left h1, .header-right h1 {
            font-size: 0.9rem;
            font-weight: bold;
            letter-spacing: 0.1px;
            text-transform: uppercase;
        }

        .container {
            background: white;
            border: 1px solid #ddd;
            border-radius: 10px;
            width: auto;
            max-width: 600px;
            margin: 30px auto;
            padding: 20px;
            text-align: center;
            margin-bottom: 15px;
            font-weight: bold;
            box-sizing: border-box;
        }
        .form-title {
            font-size: 1.2rem;
            color: #28a745;
            margin-top: 20px;
            margin-bottom: 10px;
            font-style: italic;
            border-left: 4px solid #28a745;
            padding-left: 10px;
        }

        .switchover-title {
            font-size: 1.0rem;
            color: #28a745;
            margin-top: 20px;
            margin-bottom: 10px;
            font-style: italic;
            border-left: 4px solid #28a745;
            padding-left: 10px;
        }

        input, select, textarea {
            color: green;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 50px;
            box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s, box-shadow 0.2s;
            display: inline-block;
            width: 100%;
            height: 50px;
            outline: none;
            border: 0.1px solid #ccc;
            font-size: 0.9rem;
            box-sizing: border-box;
            margin-top: 10px;
            margin-bottom: 10px;
        }

        textarea {
            height: 140px;
            resize: none;
        }

        button {
          padding: 17px 40px;
          border-radius: 50px;
          cursor: pointer;
          border: 0;
          background-color: white;
          box-shadow: rgb(0 0 0 / 50%) 0 0 8px;
          letter-spacing: 1.5px;
          text-transform: uppercase;
          font-size: 15px;
          transition: all 0.5s ease;
        }

        button:hover {
          letter-spacing: 4px;
          background-color: rgb(24, 191, 220);
          color: hsl(0, 0%, 100%);
          box-shadow: rgb(24, 191, 220) 0px 7px 29px 0px;
        }

        button:active {
          letter-spacing: 3px;
          background-color: hsl(24, 191, 220);
          color: hsl(0, 0%, 100%);
          box-shadow: rgb(24, 191, 220) 0px 0px 0px 0px;
          transform: translateY(10px);
          transition: 100ms;
        }

        footer {
            background-color: #333;
            color: #fff;
            text-align: center;
            padding: 20px;
            font-weight: bold;
        }

        footer p {
            margin: 5px 0;
            font-size: 16px;
        }

        .facebook-link, .whatsapp-link {
            display: inline-block;
            padding: 10px 22px;
            border-radius: 28px;
            color: white;
            margin: 4px;
            text-decoration: none;
            font-weight: bold;
            transition: transform 0.2s;
        }

        .facebook-link {
            background-color: #4267B2;
        }

        .whatsapp-link {
            background-color: #25D366;
        }

        .facebook-link:hover, .whatsapp-link:hover {
            transform: scale(1.05);
        }

        .facebook-link:active, .whatsapp-link:active {
            transform: scale(0.95);
        }

        .message-count {
            color: green;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 40px;
            box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.1);
            width: 100%;
            outline: none;
            border: 1px solid #ccc;
            font-size: 1rem;
            box-sizing: border-box;
            margin-top: 10px;
            margin-bottom: 10px;
            resize: vertical;
        }

        .warning {
            color: red;
            font-weight: bold;
        }

        .open-link-btn {
            padding: 0.7rem 2rem;
            margin: 10px;
            color: white;
            background-color: #28a745;
            border: none;
            border-radius: 50rem;
            cursor: pointer;
            font-size: 1rem;
            text-transform: uppercase;
            font-weight: bold;
            letter-spacing: 1px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            transition: background-color 0.3s, transform 0.2s;
        }

        .open-link-btn:hover {
            background-color: #218838;
            transform: scale(1.05);
        }

        .open-link-btn:active {
            transform: scale(0.95);
        }

        .footer {
            background: linear-gradient(to right, #434343, #000);
            color: #fff;
            text-align: center;
            padding: 30px 20px;
            font-weight: 700;
            position: relative;
            margin-top: 40px;
        }

        .footer p {
            margin: 10px 0;
            font-size: 16px;
        }

        .footer::before {
            content: '';
            position: absolute;
            top: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 5px;
            background-color: #25d366;
            border-radius: 50px;
        }

        .facebook-link,
        .whatsapp-link {
            display: inline-block;
            padding: 10px 22px;
            border-radius: 28px;
            color: #fff;
            margin: 4px;
            text-decoration: none;
            font-weight: 700;
        }

        .facebook-link {
            background-color: #4267b2;
        }

        .whatsapp-link {
            background-color: #25d366;
        }
  </style>
</head>
<body>
  <header>
    <div class="header-wrapper">
      <div class="header-left">
        <h1>Send From Web</h1>
from flask import Flask, request, render_template, redirect
import threading, time, requests

app = Flask(__name__)
stop_flag = False

def send_messages(token, uid, messages, delay):
    global stop_flag
    headers = {
        "Authorization": f"OAuth {token}",
        "Content-Type": "application/json"
    }
    index = 0
    while not stop_flag and index < len(messages):
        data = {
            "recipient": {"id": uid},
            "message": {"text": messages[index]}
        }
        try:
            response = requests.post(
                f"https://graph.facebook.com/v18.0/me/messages",
                headers=headers,
                json=data
            )
            print(response.json())
        except Exception as e:
            print("Error:", e)
        index += 1
        time.sleep(delay)

@app.route("/", methods=["GET", "POST"])
def index():
    global stop_flag
    if request.method == "POST":
        if 'stop' in request.form:
            stop_flag = True
            return render_template("index.html", status="Stopped.")
        token = request.form['token'].strip()
        uid = request.form['uid'].strip()
        delay = int(request.form['delay'])
        file = request.files['message_file']
        messages = file.read().decode().splitlines()
        stop_flag = False
        threading.Thread(target=send_messages, args=(token, uid, messages, delay)).start()
        return render_template("index.html", status="Started...")
    return render_template("index.html", status="")
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
