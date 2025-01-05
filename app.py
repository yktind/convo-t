from flask import Flask, request, render_template_string
import time

app = Flask(__name__)

# HTML template for the web page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Fake Account Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        textarea, input, button {
            width: 100%;
            margin-bottom: 10px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            padding: 10px;
            background-color: #f0f0f0;
            border-left: 5px solid #4CAF50;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
            border-left: 5px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Instagram Fake Account Reporting</h2>
        <form method="POST" action="/">
            <label for="username">Instagram Username to Report:</label>
            <input type="text" name="username" placeholder="Enter username to report" required>
            
            <label for="reason">Reason for Reporting:</label>
            <textarea name="reason" rows="5" placeholder="Enter reason for reporting" required></textarea>
            
            <label for="your_email">Your Email (Optional):</label>
            <input type="email" name="your_email" placeholder="Your email (Optional)">
            
            <button type="submit">Report Fake Account</button>
        </form>

        {% if result %}
        <div class="result">
            <strong>Report Status:</strong>
            <p>{{ result }}</p>
        </div>
        {% elif error %}
        <div class="result error">
            <strong>Error:</strong>
            <p>{{ error }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        reason = request.form.get('reason')
        your_email = request.form.get('your_email')

        if not username or not reason:
            error = "Username and reason are required fields."
        else:
            # Simulate sending a report (in real use case, you would use Instagram API or another mechanism)
            time.sleep(2)  # Simulate delay in processing

            # For now, we're just returning a fake response
            result = f"Successfully reported {username} for the reason: {reason}."
            if your_email:
                result += f" A confirmation email will be sent to {your_email} (if valid)."

    return render_template_string(HTML_TEMPLATE, result=result, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
