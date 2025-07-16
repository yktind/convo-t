from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Messenger Bot Control Panel</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- Google Font -->
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">

    <style>
        body {
            margin: 0;
            padding: 0;
            background: url('https://images.unsplash.com/photo-1549921296-3a6b77b60e78') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Orbitron', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            color: #fff;
            overflow-x: hidden;
        }

        .glass-box {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 40px;
            width: 90%;
            max-width: 500px;
            backdrop-filter: blur(15px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
        }

        h1 {
            font-size: 32px;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px #000;
        }

        input, button {
            width: 100%;
            padding: 15px;
            margin-top: 15px;
            border-radius: 12px;
            border: none;
            outline: none;
            font-size: 16px;
        }

        input {
            background: rgba(255, 255, 255, 0.2);
            color: #fff;
            box-shadow: inset 0 0 10px rgba(255,255,255,0.2);
        }

        input::placeholder {
            color: #ddd;
        }

        button {
            background: linear-gradient(145deg, #00c6ff, #0072ff);
            color: white;
            cursor: pointer;
            transition: 0.4s ease-in-out;
            font-weight: bold;
            box-shadow: 0 8px 20px rgba(0, 114, 255, 0.6), 0 4px 10px rgba(0,0,0,0.4);
        }

        button:hover {
            transform: scale(1.05);
            background: linear-gradient(145deg, #0072ff, #00c6ff);
            box-shadow: 0 12px 24px rgba(0,114,255,0.7);
        }

        @media screen and (max-width: 600px) {
            .glass-box {
                padding: 25px;
            }

            h1 {
                font-size: 26px;
            }
        }
    </style>
</head>
<body>
    <div class="glass-box">
        <h1>🤖 Messenger Bot Panel</h1>
        <form method="post">
            <input type="text" name="token" placeholder="🔑 Enter Access Token" required>
            <input type="text" name="thread_id" placeholder="💬 Enter Thread ID" required>
            <input type="text" name="message" placeholder="✉️ Enter Message" required>
            <button type="submit">🚀 Send Message</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    if app.debug:
        print("Flask Debug Mode Active")
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
  
