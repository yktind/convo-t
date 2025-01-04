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
    <title>Facebook Token Extractor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
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
        input, button {
            width: 100%;
            margin-bottom: 10px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            border: none;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            padding: 10px;
            background: #e3f2fd;
            border-left: 4px solid #2196F3;
        }
        .error {
            margin-top: 20px;
            padding: 10px;
            background: #f8d7da;
            border-left: 4px solid #f44336;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Facebook Token Extractor</h2>
        <form method="POST">
            <label for="cookies">Enter Your Facebook Cookies:</label>
            <input type="text" name="cookies" id="cookies" placeholder="Paste your Facebook cookies here" required>
            <button type="submit">Extract Token</button>
        </form>
        {% if token %}
        <div class="result">
            <strong>Extracted Token:</strong>
            <p>{{ token }}</p>
        </div>
        {% elif error %}
        <div class="error">
            <strong>Error:</strong>
            <p>{{ error }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

# Route for Displaying the Web Page
@app.route('/', methods=['GET', 'POST'])
def index():
    token = None
    error = None

    if request.method == 'POST':
        cookies = request.form.get('cookies', '').strip()

        if not cookies:
            error = "Cookies are required."
        else:
            try:
                token = extract_token(cookies)
                if not token:
                    error = "Failed to extract token. Please check your cookies."
            except Exception as e:
                error = f"An error occurred: {e}"

    return render_template_string(HTML_TEMPLATE, token=token, error=error)

# Function to Extract the Access Token
def extract_token(cookies):
    url = "https://business.facebook.com/business_locations"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Convert cookies string into a dictionary
    cookies_dict = {}
    for item in cookies.split(';'):
        key, value = item.strip().split('=', 1)
        cookies_dict[key] = value

    # Make a request to Facebook to extract the token
    response = requests.get(url, headers=headers, cookies=cookies_dict)
    if response.status_code == 200:
        match = re.search(r'"EAAB\w+"', response.text)
        if match:
            return match.group(0).strip('"')
    return None

# Run the Flask App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
