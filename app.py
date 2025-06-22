
from flask import Flask, request, render_template_string
import requests
import time
import re

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>Messenger Bot (via Cookie)</title>
  <style>
    body { font-family: Arial; padding: 20px; background: #f4f4f4; }
    form { background: white; padding: 20px; border-radius: 10px; max-width: 500px; margin: auto; box-shadow: 0 0 8px rgba(0,0,0,0.1); }
    input, textarea { width: 100%; padding: 10px; margin-top: 10px; border-radius: 5px; border: 1px solid #ccc; }
    button { padding: 10px; background: #4CAF50; color: white; border: none; border-radius: 5px; margin-top: 10px; cursor: pointer; }
    button:hover { background: #45a049; }
  </style>
</head>
<body>
  <h2>ðŸª Messenger Bot - Cookie Based</h2>
  <form method='POST'>
    <label>ðŸª Facebook Cookie:</label>
    <textarea name='cookie' rows='4' required></textarea>

    <label>ðŸŽ¯ Target UID:</label>
    <input type='text' name='uid' required>

    <label>âœï¸ Message:</label>
    <textarea name='message' rows='3' required></textarea>

    <label>â±ï¸ Delay (seconds):</label>
    <input type='number' name='delay' value='2' step='0.5'>

    <button type='submit'>ðŸš€ Send Message</button>
  </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cookie = request.form["cookie"]
        uid = request.form["uid"]
        message = request.form["message"]
        delay = float(request.form["delay"])
        result = send_message_with_cookie(cookie, uid, message)
        time.sleep(delay)
        return f"<h3>âœ… Result:</h3><p>{result}</p><a href='/'>â¬…ï¸ Go Back</a>"
    return render_template_string(HTML_PAGE)

def send_message_with_cookie(cookie_str, target_id, message_text):
    try:
        cookies = {c.split("=")[0].strip(): c.split("=")[1] for c in cookie_str.split(";") if "=" in c}
        c_user = cookies.get("c_user")
        fb_dtsg = get_fb_dtsg(cookies)
        if not fb_dtsg:
            return "âŒ Failed to extract fb_dtsg token."

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile)",
        }
        data = {
            "fb_dtsg": fb_dtsg,
            "body": message_text,
            "tids": f"cid.c.{c_user}:{target_id}",
            "wwwupp": "C3",
            "platform_xmd": "",
            "target": target_id,
            "c": "1",
            "csid": str(int(time.time() * 1000)),
            "messages[0]": message_text,
            "action_type": "ma-type:user-generated-message",
            "client": "mercury",
            "timestamp": str(int(time.time() * 1000)),
            "source": "source:chat:web",
        }
        res = requests.post("https://www.facebook.com/messages/send/", headers=headers, data=data, cookies=cookies)
        return f"{res.status_code} - {res.text[:200]}"

    except Exception as e:
        return f"âŒ Exception: {str(e)}"

def get_fb_dtsg(cookies):
    try:
        res = requests.get("https://www.facebook.com", cookies=cookies)
        match = re.search(r'name="fb_dtsg" value="(.*?)"', res.text)
        return match.group(1) if match else None
    except:
        return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
