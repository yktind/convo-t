from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = """
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
            padding: 20px;
        }
        .container {
            max-width: 500px;
            background-color: #fff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            margin: 20px auto;
        }
        .btn-submit {
            width: 100%;
            background-color: #007bff;
            color: #fff;
            border: none;
            padding: 10px;
            font-size: 1rem;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        .btn-submit:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2 class="text-center">Facebook Token Extractor</h2>
        <form action="/get-token" method="post">
            <div class="mb-3">
                <label for="cookies" class="form-label">Enter Facebook Cookies:</label>
                <textarea class="form-control" id="cookies" name="cookies" rows="5" placeholder="Paste your Facebook cookies here..." required></textarea>
            </div>
            <button type="submit" class="btn btn-primary btn-submit">Extract Token</button>
        </form>
    </div>
</body>
</html>
"""

# Helper function to simulate token extraction
def extract_token_from_cookies(cookies):
    # Placeholder logic for token extraction
    if "EAAB" in cookies:
        return "EAABSampleToken123456789"  # Replace with actual extraction logic
    return None

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/get-token", methods=["POST"])
def get_token():
    cookies = request.form.get("cookies")
    if not cookies:
        return jsonify({"error": "Cookies not provided"}), 400

    # Extract token from cookies
    token = extract_token_from_cookies(cookies)
    if token:
        return jsonify({"success": True, "token": token}), 200
    else:
        return jsonify({"error": "Unable to extract token"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
