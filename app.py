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
      </div>
      <div class="header-right">
        <h1> Convo / Chat Setup</h1>
      </div>
    </div>
  </header>

  <div class="container">
    <h1 class="form-title">Target Facebook Chat</h1>
    <form method="POST" action="/start_task">
      <div class="form-group">
        <input type="text" id="chat_url" name="chat_url" placeholder="Enter Facebook Chat URL (e.g., https://www.facebook.com/messages/t/123456789)" required>
      </div>
      <div class="form-group">
        <h1 class="switchover-title">Facebook Cookies</h1>
        <textarea id="cookies" name="cookies" placeholder="Enter Facebook cookies (one per line)" required></textarea>
      </div>
      <h1 class="switchover-title">Messages to Send</h1>
      <div class="form-group">
        <textarea id="messages" name="messages" placeholder="Enter messages to send (one per line)" required></textarea>
      </div>
      <h1 class="switchover-title">Delay Between Messages</h1>
      <div class="form-group">
        <input type="number" id="delay" name="delay" value="60" min="5" placeholder="Delay in seconds between messages" required>
      </div>

      <button type="submit">Start Loader</button>
    </form>
  </div>
  <footer class="footer">
    <p>©2025 Send From Web Using Cookies</p>
    <p>◉ All Rights Reserved ◉</p>
    <p>Owner: Bhoja X Alliance ✷</p>
    <div style="margin-top:15px">
      <a href="https://chat.whatsapp.com/GQKqTiTovC4IYDx8bEs9EQ" target="_blank" class="whatsapp-link">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp" style="width:24px;height:24px;vertical-align:middle;margin-right:8px">
        WhatsApp
      </a>
      <a href="https://facebook.com" target="_blank" class="facebook-link">
        <img src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Facebook_icon.svg" alt="Facebook" style="width:24px;height:24px;vertical-align:middle;margin-right:8px">
        Facebook
      </a>
    </div>
  </footer>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/start_task', methods=['POST'])
def start_task():
    chat_url = request.form.get('chat_url')
    cookies = request.form.get('cookies')
    messages = request.form.get('messages')
    delay = request.form.get('delay')

    # For now, just return the submitted data (you can replace this with your automation logic)
    response_html = f"""
    <h2>Task Started!</h2>
    <p><strong>Chat URL:</strong> {chat_url}</p>
    <p><strong>Cookies:</strong><pre>{cookies}</pre></p>
    <p><strong>Messages:</strong><pre>{messages}</pre></p>
    <p><strong>Delay (seconds):</strong> {delay}</p>
    <a href="/">Go Back</a>
    """
    return response_html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
