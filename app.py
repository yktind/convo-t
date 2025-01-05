from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# HTML Template for the Web Page
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
            background-color: #fff;
            border-radius: 10px;
            padding: 20px;
            margin: 20px auto;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .btn-submit {
            width: 100%;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #6c757d;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2 class="text-center">Facebook Token Extractor</h2>
        <form action="/extract" method="post">
            <div class="mb-3">
                <label for="cookies" class="form-label">Enter Facebook Cookies:</label>
                <textarea class="form-control" id="cookies" name="cookies" rows="5" placeholder="Paste your Facebook cookies here..." required></textarea>
            </div>
            <button type="submit" class="btn btn-primary btn-submit">Extract Tokens</button>
        </form>
    </div>
    <div class="footer">
        <p>&copy; 2025 Developed by DeViL BoY. All Rights Reserved.</p>
    </div>
</body>
</html>
"""

# Token Extraction Logic
def extract_tokens(cookies):
    """
    Extract token-like substrings from the provided cookies string.
    Looks for patterns starting with 'EAAG', 'EAAB', etc.
    """
    tokens = {}
    for token_prefix in ['EAAG', 'EAAB', 'EAAD', 'EAAC', 'EAAF', 'EABB']:
        if token_prefix in cookies:
            start_idx = cookies.find(token_prefix)
            end_idx = cookies.find(';', start_idx)
            if end_idx == -1:
                end_idx = len(cookies)
            tokens[token_prefix] = cookies[start_idx:end_idx]
    return tokens

# Flask Routes
@app.route('/', methods=['GET'])
def home():
    """Render the HTML form."""
    return render_template_string(html_template)

@app.route('/extract', methods=['POST'])
def extract():
    """Extract tokens from the provided cookies."""
    cookies = request.form.get('cookies', '')
    if not cookies:
        return jsonify({'error': 'No cookies provided.'}), 400
    
    tokens = extract_tokens(cookies)
    if tokens:
        return jsonify({'status': 'success', 'tokens': tokens})
    else:
        return jsonify({'status': 'failed', 'message': 'No tokens found in the cookies.'})

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
