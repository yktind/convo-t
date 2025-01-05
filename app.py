import requests
from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

# HTML Template for the Web Page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Fake Account Checker</title>
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
        textarea, button {
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
        <h2>Instagram Fake Account Checker</h2>
        <form method="POST" action="/">
            <label for="cookies">Enter Instagram Cookies:</label>
            <textarea name="cookies" rows="8" placeholder="Paste your Instagram cookies here..." required></textarea>
            <button type="submit">Check Account</button>
        </form>
        {% if result %}
        <div class="result">
            <strong>Account Status:</strong>
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

# Function to check if an account is fake based on a simple heuristic (low followers)
def check_fake_account(cookies):
    try:
        # Send a request to Instagram's profile page to retrieve account data
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
        }

        # Dummy Instagram profile URL for user to test (e.g., change this to a real profile URL)
        profile_url = 'https://www.instagram.com/{}/'.format(cookies)  # Normally, this would be the Instagram username
        
        response = requests.get(profile_url, cookies={'cookie': cookies}, headers=headers)
        
        if response.status_code != 200:
            raise Exception("Failed to load Instagram profile.")
        
        # You could scrape profile details here. For simplicity, we will check if "followers" exist in the page
        if 'followers' not in response.text:
            return "Unable to retrieve account data."

        # Check followers count (simplified logic)
        followers_count_match = re.search(r'\"followers_count\":(\d+)', response.text)
        if followers_count_match:
            followers_count = int(followers_count_match.group(1))
            if followers_count < 50:
                return "This account is flagged as fake (low followers)."
            return "This account seems legit."
        else:
            return "Unable to check followers count."
    
    except Exception as e:
        print(f"Error checking account: {e}")
        return "Error checking account."

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        cookies = request.form.get('cookies', '').strip()
        if not cookies:
            error = "Please provide Instagram cookies."
        else:
            result = check_fake_account(cookies)
    
    return render_template_string(HTML_TEMPLATE, result=result, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
