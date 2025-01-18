from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cookie Parser & Token Extractor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            color: #333;
            text-align: center;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: auto;
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        textarea, input {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            background-color: #007BFF;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .result {
            text-align: left;
            margin-top: 20px;
            background: #f9f9f9;
            padding: 15px;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Cookie Parser & Token Extractor</h1>
        <form method="POST">
            <textarea name="cookie_string" placeholder="Paste your cookie string here..." rows="5" required></textarea>
            <button type="submit">Parse</button>
        </form>
        {% if cookies %}
            <div class="result">
                <h3>Parsed Cookies (JSON):</h3>
                <pre>{{ cookies }}</pre>
                <h3>Extracted Token:</h3>
                <pre>{{ token }}</pre>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def cookie_parser():
    cookies = None
    token = None

    if request.method == 'POST':
        cookie_string = request.form.get('cookie_string')
        cookies = {}
        
        # Parse the cookie string
        try:
            for item in cookie_string.split(';'):
                key, value = item.split('=', 1)
                cookies[key.strip()] = value.strip()
        except Exception as e:
            return f"Error parsing cookies: {e}", 400

        # Extract the token (assuming it starts with 'EAAB')
        token = next((v for k, v in cookies.items() if v.startswith('EAAB')), "No token found")

    return render_template_string(HTML_TEMPLATE, cookies=jsonify(cookies).get_data(as_text=True), token=token)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
