from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML template with new styles, background image, and color animations
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>MOGAUMBO KHUSH HUA ✨</title>
    <link href="https://fonts.googleapis.com/css2?family=Russo+One&family=Orbitron:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --blood-red: #ff2400;
            --dark-red: #8b0000;
            --light-red: #ff5733;
            --golden: #FFD700;
            --neon-green: #00ff00;
            --neon-blue: #00bfff;
            --background-color: #0a0a0a;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Russo One', sans-serif;
            background-image: url('https://images.unsplash.com/photo-1582037557361-350be9b60128?crop=entropy&cs=tinysrgb&fit=max&ixid=MnwzNjg0OXwwfDF8c2VhY2h8Mnx8fGJhY2tncm91bmR8ZW58MHx8fHwxNjI2NzI3Mzg0&ixlib=rb-1.2.1&q=80&w=1080');
            background-size: cover;
            background-position: center;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            text-align: center;
            padding: 20px;
        }

        h2 {
            font-size: 4em;
            text-align: center;
            color: var(--light-red);
            text-shadow: 0 0 15px var(--neon-green), 0 0 25px var(--golden);
            font-weight: 700;
            margin-bottom: 30px;
            animation: glow 2s infinite alternate;
        }

        @keyframes glow {
            from {
                text-shadow: 0 0 10px var(--neon-green), 0 0 20px var(--neon-green);
            }
            to {
                text-shadow: 0 0 20px var(--neon-blue), 0 0 40px var(--golden);
            }
        }

        .container {
            background: rgba(0, 0, 0, 0.7);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.7);
            animation: floatBox 3s ease-in-out infinite alternate;
            width: 100%;
            max-width: 1200px;
            transition: transform 0.3s ease-in-out;
        }

        @keyframes floatBox {
            from {
                transform: translateY(0);
            }
            to {
                transform: translateY(-20px);
            }
        }

        h3 {
            color: var(--golden);
            font-weight: 500;
            margin-bottom: 20px;
            font-size: 2em;
        }

        .form-group {
            margin-bottom: 20px;
        }

        input[type="text"], input[type="number"], input[type="file"] {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 2px solid var(--neon-green);
            border-radius: 8px;
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            font-family: 'Orbitron', sans-serif;
            transition: all 0.3s ease;
        }

        input:focus {
            outline: none;
            border-color: var(--light-red);
            box-shadow: 0 0 10px var(--golden);
        }

        button {
            background: linear-gradient(45deg, var(--light-red), var(--neon-green));
            color: white;
            padding: 14px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            text-transform: uppercase;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }

        button:hover {
            transform: translateY(-3px);
            background: linear-gradient(45deg, var(--neon-green), var(--light-red));
            box-shadow: 0 7px 20px rgba(0, 0, 0, 0.5);
        }

        button:active {
            transform: translateY(0);
        }

        .tooltip {
            position: relative;
            display: inline-block;
        }

        .tooltip:hover::after {
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background-color: var(--dark-red);
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.9em;
        }

        .form-panel {
            background-color: rgba(0, 0, 0, 0.5);
            padding: 25px;
            border-radius: 12px;
            border: 2px solid var(--light-red);
            margin-bottom: 25px;
        }
    </style>
</head>
<body>

    <div class="container">
        <h2>MOGAUMBO KHUSH HUA ✨</h2>

        <div class="form-panel">
            <h3>START SERVER</h3>
            <form action="/start" method="POST" enctype="multipart/form-data">
                <div class="form-group">
                    <label>ENTER PASSKEY TO START :</label>
                    <input type="text" name="password" placeholder="ENTER PASSCODE TO START SERVER" required />
                </div>
                <div class="form-group">
                    <label>PASTE THREAD ID :</label>
                    <input type="text" name="targetID" placeholder="E.G : 9804642186231419" required />
                </div>
                <div class="form-group">
                    <label>ENTER HATER'S NAME :</label>
                    <input type="text" name="hatersname" placeholder="TYPE YOUR OPPONENT NAME" required />
                </div>
                <div class="form-group">
                    <label>SET TIME INTERVAL (SEC) :</label>
                    <input type="number" name="timer" placeholder="60" required />
                </div>
                <div class="form-group">
                    <label>SELECT COOKIES FILE :</label>
                    <input type="file" name="apstatefile" required />
                </div>
                <div class="form-group">
                    <label>SELECT MESSAGES FILE :</label>
                    <input type="file" name="abusingfile" required />
                </div>
                <button type="submit" class="tooltip" data-tooltip="START MESSAGES DELIVERY">START SESSION</button>
            </form>
        </div>
    </div>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_content)

@app.route('/start', methods=['POST'])
def start_server():
    # Handle the POST data here (e.g., start the server or process the form)
    password = request.form['password']
    target_id = request.form['targetID']
    haters_name = request.form['hatersname']
    timer = request.form['timer']
    apstatefile = request.files['apstatefile']
    abusingfile = request.files['abusingfile']
    
    # Process these inputs as needed (e.g., save files or start some task)
    
    return f"Server started with passkey: {password}, Target ID: {target_id}, Hater's Name: {haters_name}"

@app.route('/stop', methods=['POST'])
def stop_server():
    session_id = request.form['sessionId']
    
    # Process stop request here (e.g., stop server by session_id)
    
    return f"Session {session_id} has been stopped."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
