from flask import Flask, request, render_template_string
import re
import requests

app = Flask(__name__)

# HTML Template for the Web Page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Access Token Extractor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background: white;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        label {
            font-weight: bold;
        }
        textarea, button {
            width: 100%;
            margin: 10px 0;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background: #45a049;
        }
        .output {
            margin-top: 20px;
            padding: 10px;
            background: #f1f1f1;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Facebook Token Extractor</h1>
        <form method="POST" action="/">
            <label for="cookies">Enter Facebook Cookies:</label>
            <textarea name="cookies" id="cookies" rows="5" placeholder="Paste your Facebook cookies here" required></textarea>
            <button type="submit">Extract Token</button>
        </form>
        {% if token %}
        <div class="output">
            <h3>Extracted Token:</h3>
            <p>{{ token }}</p>
        </div>
        {% elif error %}
        <div class="output">
            <h3>Error:</h3>
            <p>{{ error }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

# Function to extract the EAAB token
def extract_token(cookies):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = "https://business.facebook.com/business_locations"
    cookies_dict = {"cookie": cookies}
    
    try:
        response = requests.get(url, headers=headers, cookies=cookies_dict)
        if response.status_code == 200:
            token_match = re.search(r'(EAAB\w+)', response.text)
            if token_match:
                return token_match.group(1)
            return None
        return None
    except Exception as e:
        return str(e)

@app.route("/", methods=["GET", "POST"])
def index():
    token = None
    error = None
    if request.method == "POST":
        cookies = request.form.get("cookies")
        if cookies:
            token = extract_token(cookies)
            if not token:
                error = "Failed to extract token. Please check your cookies."
        else:
            error = "No cookies provided."
    return render_template_string(HTML_TEMPLATE, token=token, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
