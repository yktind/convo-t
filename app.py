from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def extract_token():
    if request.method == "POST":
        cookies = request.form.get("cookies", "").strip()
        if not cookies:
            return jsonify({"error": "Cookies are required."}), 400

        try:
            # Extract EAAG token from cookies
            token = extract_eaag_token(cookies)
            if token:
                return jsonify({"token": token})
            else:
                return jsonify({"error": "Failed to extract token. Please check your cookies."}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Render form to input cookies
    return '''
    <html>
    <head>
        <title>Facebook Token Extractor</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background-color: #f9f9f9; }
            .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
            input, button, textarea { width: 100%; margin-bottom: 10px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
            button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
            button:hover { background-color: #45a049; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Facebook EAAG Token Extractor</h2>
            <form method="POST" action="/">
                <label for="cookies">Enter Cookies:</label>
                <textarea name="cookies" placeholder="Paste your Facebook cookies here..." required></textarea>
                <button type="submit">Extract Token</button>
            </form>
        </div>
    </body>
    </html>
    '''

def extract_eaag_token(cookies):
    """
    Extracts the EAAG token from the provided cookies.
    """
    import re
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
        ),
    }

    # Simulate a request to a Facebook endpoint
    response = requests.get(
        "https://business.facebook.com/business_locations",
        headers=headers,
        cookies=parse_cookies(cookies),
    )

    # Look for EAAG token in the response
    token_match = re.search(r'EAAG\w+', response.text)
    return token_match.group(0) if token_match else None

def parse_cookies(cookies):
    """
    Parses a string of cookies into a dictionary.
    """
    cookies_dict = {}
    for cookie in cookies.split(";"):
        if "=" in cookie:
            key, value = cookie.strip().split("=", 1)
            cookies_dict[key] = value
    return cookies_dict

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
