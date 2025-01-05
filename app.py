from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Helper function to extract tokens from cookies
def extract_tokens(cookie):
    tokens = {
        "TokenEAAG": None,
        "TokenEAAB": None,
        "TokenEAAD": None,
        "TokenEAAC": None,
        "TokenEAAF": None,
        "TokenEABB": None
    }
    for token in tokens.keys():
        if token in cookie:
            tokens[token] = cookie.split(token + "=")[1].split(";")[0]
    return tokens

# HTML template for the form
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Token Extractor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
            font-family: Arial, sans-serif;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body>
    <div class="container">
        <h2 class="text-center mb-4">Facebook Cookie Token Extractor</h2>
        <form method="POST" action="/">
            <div class="mb-3">
                <label for="cookie" class="form-label">Enter Facebook Cookie:</label>
                <textarea class="form-control" id="cookie" name="cookie" rows="5" placeholder="Paste your Facebook cookies here..." required></textarea>
            </div>
            <button type="submit" class="btn btn-primary w-100">Extract Tokens</button>
        </form>
        {% if tokens %}
            <div class="mt-4">
                <h4>Extracted Tokens:</h4>
                <pre>{{ tokens }}</pre>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    tokens = None
    if request.method == "POST":
        cookie = request.form.get("cookie", "")
        tokens = extract_tokens(cookie)
    return render_template_string(html_template, tokens=tokens)

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
