from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cookie Extractor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
            font-family: Arial, sans-serif;
        }
        .container {
            margin-top: 50px;
            max-width: 600px;
            background: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Cookie Extractor Tool</h1>
            <p>Extract and display Facebook cookies</p>
        </div>
        <form action="/extract" method="post">
            <div class="mb-3">
                <label for="cookieInput" class="form-label">Paste Your Cookies Here:</label>
                <textarea class="form-control" id="cookieInput" name="cookies" rows="5" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary w-100">Extract Cookies</button>
        </form>
        {% if cookies %}
        <div class="mt-4">
            <h4>Extracted Cookies:</h4>
            <ul class="list-group">
                {% for key, value in cookies.items() %}
                <li class="list-group-item"><strong>{{ key }}:</strong> {{ value }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
    </div>
    <footer class="footer">
        <p>&copy; 2024 Cookie Extractor. All rights reserved.</p>
    </footer>
</body>
</html>
"""

# Route for the main page
@app.route("/", methods=["GET", "POST"])
def index():
    extracted_cookies = {}
    if request.method == "POST":
        cookie_string = request.form.get("cookies", "")
        extracted_cookies = parse_cookies(cookie_string)
    return render_template_string(HTML_TEMPLATE, cookies=extracted_cookies)

# Function to parse cookie string into a dictionary
def parse_cookies(cookie_string):
    cookies = {}
    try:
        for item in cookie_string.split(";"):
            key, value = item.strip().split("=", 1)
            cookies[key.strip()] = value.strip()
    except Exception as e:
        print(f"Error parsing cookies: {e}")
    return cookies

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
