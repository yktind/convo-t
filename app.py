from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup as sop
import re

app = Flask(__name__)

# HTML template for the webpage
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
        input, button, textarea {
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
            <label for="username">Enter Instagram Username:</label>
            <input type="text" name="username" placeholder="Enter Instagram Username" required>
            <button type="submit">Check Account</button>
        </form>
        {% if result %}
        <div class="result">
            <h3>Account Status: {{ result['status'] }}</h3>
            <p><strong>Profile Name:</strong> {{ result['name'] }}</p>
            <p><strong>Followers:</strong> {{ result['followers'] }}</p>
            <p><strong>Following:</strong> {{ result['following'] }}</p>
            <p><strong>Posts:</strong> {{ result['posts'] }}</p>
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

# Function to fetch Instagram profile data
def fetch_instagram_data(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None

        soup = sop(response.text, "html.parser")
        script_tag = soup.find("script", text=re.compile("window\._sharedData"))
        if not script_tag:
            return None
        
        shared_data = re.findall(r'window\._sharedData = ({.*?});', script_tag.string)[0]
        data = eval(shared_data)  # This will parse the JSON data
        
        user_data = data['entry_data']['ProfilePage'][0]['graphql']['user']
        return user_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Function to check the account's authenticity based on basic profile data
def check_account_authenticity(user_data):
    status = "Suspicious Account"
    if user_data:
        followers = user_data['edge_followed_by']['count']
        following = user_data['edge_follow']['count']
        posts = user_data['edge_owner_to_timeline_media']['count']
        name = user_data['full_name']

        # Fake account heuristics (for example purposes)
        if followers < 100 and following > 1000:
            status = "Fake Account"
        elif posts == 0 and followers < 50:
            status = "Likely Fake Account"
        else:
            status = "Legitimate Account"
        
        return {
            'status': status,
            'name': name,
            'followers': followers,
            'following': following,
            'posts': posts
        }
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        username = request.form.get('username').strip()
        user_data = fetch_instagram_data(username)
        if user_data:
            result = check_account_authenticity(user_data)
        else:
            error = "Account not found or failed to retrieve data. Please check the username."

    return render_template_string(HTML_TEMPLATE, result=result, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
