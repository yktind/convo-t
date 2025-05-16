from flask import Flask, request, Response

app = Flask(__name__)

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Welcome to WaR RuLeX SeRveR</title>
<style>
body { font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 0; }
.container { max-width: 600px; margin: 50px auto; padding: 20px; background-color: #fff; border-radius: 5px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
h1 { text-align: center; margin-bottom: 20px; }
.menu { text-align: center; margin-bottom: 20px; }
.menu button { padding: 10px 20px; background-color: #007bff; color: #fff; border: none; border-radius: 5px; cursor: pointer; transition: background-color 0.3s; margin-right: 10px; }
.menu button:hover { background-color: #0056b3; }
form { margin-top: 20px; display: none; }
label { display: block; margin-bottom: 5px; font-weight: bold; }
input[type="text"], input[type="number"], textarea { width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; }
input[type="submit"] { width: 100%; padding: 10px; background-color: #007bff; color: #fff; border: none; border-radius: 5px; cursor: pointer; transition: background-color 0.3s; }
input[type="submit"]:hover { background-color: #0056b3; }
.footer { background-color: #333; color: #fff; text-align: center; padding: 20px; bottom: 0; left: 0; width: 100%; }
.whatsapp-link { color: #fff; text-decoration: none; margin-right: 10px; }
.whatsapp-link i { margin-right: 5px; }
.image-container img { max-width: 100%; height: auto; display: block; margin: 0 auto; }
</style>
</head>
<body>
<div class="container">
<div class="image-container">
<img src="https://i.ibb.co/TKg06Q9/851aca8a5cc97e47ee3afc92866f421c.jpg" alt="Image">
</div>
<h1>Welcome to WaR RuLeX </h1>
<div class="menu">
<button id="commentBtn">Post</button>
<button id="convoBtn">Convo</button>
</div>
<form id="commentForm" action="/post_comments" method="POST" enctype="multipart/form-data">
<label for="cookie">Cookie:</label>
<input type="text" id="cookie" name="cookie" required>
<label for="post_id">Post ID:</label>
<input type="text" id="post_id" name="post_id" required>
<label for="delay">Delay (seconds):</label>
<input type="number" id="delay" name="delay" min="1" value="1" required>
<label for="hattersname">Hatter's Name:</label>
<input type="text" id="hattersname" name="hattersname" required>
<label for="comments">Comments:</label>
<textarea id="comments" name="comments" rows="4" cols="50" required></textarea>
<input type="submit" value="Start Comment Sending">
</form>
<form id="convoForm" action="/convo_inbox" method="POST" enctype="multipart/form-data">
<label for="accessToken">Access Token:</label>
<input type="text" id="accessToken" name="accessToken" required>
<label for="threadId">Thread ID:</label>
<input type="text" id="threadId" name="threadId" required>
<label for="haterName">Your Name:</label>
<input type="text" id="haterName" name="haterName" required>
<label for="txtFile">Messages File:</label>
<input type="file" id="txtFile" name="txtFile" accept=".txt" required>
<label for="delay">Delay (seconds):</label>
<input type="number" id="delay" name="delay" min="1" value="1" required>
<input type="submit" value="Start Convo Sending">
</form>
</div>
<footer class="footer">
<p>© 2024 FREE TRICKS DEVIL. All Rights Reserved.</p>
<p>Made with by <a href="https://www.facebook.com/BL9CK.D3VIL">Facebook</a></p>
<div class="mb-3">
<a href="https://wa.me/+917668337116" class="whatsapp-link"><i class="fab fa-whatsapp"></i> Chat on WhatsApp</a>
</div>
</footer>
<script>
const commentBtn = document.getElementById('commentBtn');
const convoBtn = document.getElementById('convoBtn');
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Welcome to WaR RuLeX SeRveR</title>
<style>
body {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    background: linear-gradient(270deg, #1e3c72, #2a5298);
    background-size: 400% 400%;
    animation: gradientAnimation 15s ease infinite;
    color: #fff;
}
@keyframes gradientAnimation {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.container {
    max-width: 700px;
    margin: 60px auto;
    background: rgba(0, 0, 0, 0.7);
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0 0 25px rgba(0,0,0,0.5);
}
h1 {
    text-align: center;
    margin-bottom: 30px;
    color: #00ffd0;
    text-shadow: 0 0 10px #00ffd0;
}
.menu {
    text-align: center;
    margin-bottom: 25px;
}
.menu button {
    padding: 12px 25px;
    margin: 0 10px;
    border: none;
    border-radius: 30px;
    background-color: #00c6ff;
    color: #fff;
    font-size: 16px;
    cursor: pointer;
    box-shadow: 0 0 10px #00c6ff;
    transition: all 0.3s ease;
}
.menu button:hover {
    background-color: #0073e6;
    box-shadow: 0 0 20px #00c6ff;
}
form {
    display: none;
}
label {
    font-weight: bold;
    margin-top: 10px;
    display: block;
}
input[type="text"],
input[type="number"],
textarea,
input[type="file"] {
    width: 100%;
    padding: 10px;
    margin: 8px 0 15px;
    border-radius: 5px;
    border: none;
    box-sizing: border-box;
}
input[type="submit"] {
    background-color: #00c6ff;
    color: #fff;
    padding: 12px;
    border: none;
    border-radius: 30px;
    font-size: 16px;
    cursor: pointer;
    width: 100%;
    box-shadow: 0 0 10px #00c6ff;
}
input[type="submit"]:hover {
    background-color: #0073e6;
}
.footer {
    background-color: rgba(0,0,0,0.8);
    padding: 20px;
    text-align: center;
    color: #ccc;
    margin-top: 30px;
    border-top: 1px solid #444;
}
.footer a {
    color: #00c6ff;
    text-decoration: none;
}
.image-container img {
    max-width: 100%;
    height: auto;
    border-radius: 15px;
    box-shadow: 0 0 15px rgba(0,0,0,0.6);
    margin-bottom: 20px;
}
</style>
</head>
<body>
<div class="container">
<div class="image-container">
<img src="https://i.ibb.co/TKg06Q9/851aca8a5cc97e47ee3afc92866f421c.jpg" alt="Image">
</div>
<h1>Welcome to WaR RuLeX</h1>
<div class="menu">
<button id="commentBtn">Post</button>
<button id="convoBtn">Convo</button>
</div>

<!-- Post Comments Form -->
<form id="commentForm" action="/post_comments" method="POST" enctype="multipart/form-data">
<label for="cookie">Cookie:</label>
<input type="text" id="cookie" name="cookie" required>
<label for="post_id">Post ID:</label>
<input type="text" id="post_id" name="post_id" required>
<label for="delay">Delay (seconds):</label>
<input type="number" id="delay" name="delay" min="1" value="1" required>
<label for="hattersname">Hatter's Name:</label>
<input type="text" id="hattersname" name="hattersname" required>
<label for="comments">Comments:</label>
<textarea id="comments" name="comments" rows="4" cols="50" required></textarea>
<input type="submit" value="Start Comment Sending">
</form>

<!-- Convo Form -->
<form id="convoForm" action="/convo_inbox" method="POST" enctype="multipart/form-data">
<label for="accessToken">Access Token:</label>
<input type="text" id="accessToken" name="accessToken" required>
<label for="threadId">Thread ID:</label>
<input type="text" id="threadId" name="threadId" required>
<label for="haterName">Your Name:</label>
<input type="text" id="haterName" name="haterName" required>
<label for="txtFile">Messages File:</label>
<input type="file" id="txtFile" name="txtFile" accept=".txt" required>
<label for="delay">Delay (seconds):</label>
<input type="number" id="delay" name="delay" min="1" value="1" required>
<input type="submit" value="Start Convo Sending">
</form>
</div>
<footer class="footer">
<p>© 2024 FREE TRICKS DEVIL. All Rights Reserved.</p>
<p>Made with by <a href="https://www.facebook.com/BL9CK.D3VIL">Facebook</a></p>
<a href="https://wa.me/+917668337116" class="whatsapp-link">Chat on WhatsApp</a>
</footer>
<script>
const commentBtn = document.getElementById('commentBtn');
const convoBtn = document.getElementById('convoBtn');
const commentForm = document.getElementById('commentForm');
const convoForm = document.getElementById('convoForm');
commentForm.style.display = 'none';
convoForm.style.display = 'none';
commentBtn.addEventListener('click', function() {
    commentForm.style.display = 'block';
    convoForm.style.display = 'none';
});
convoBtn.addEventListener('click', function() {
    convoForm.style.display = 'block';
    commentForm.style.display = 'none';
});
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return Response(HTML_CONTENT, mimetype='text/html')

@app.route('/post_comments', methods=['POST'])
def post_comments():
    data = request.form
    cookie = data.get('cookie')
    post_id = data.get('post_id')
    delay = data.get('delay')
    hattersname = data.get('hattersname')
    comments = data.get('comments')
    # Dummy print or log for demo
    print(f"Comment Request: {cookie=}, {post_id=}, {delay=}, {hattersname=}, {comments=}")
    return "Comment request received."

@app.route('/convo_inbox', methods=['POST'])
def convo_inbox():
    data = request.form
    file = request.files['txtFile']
    content = file.read().decode('utf-8')
    # Dummy print or log for demo
    print(f"Convo Request: {data.get('accessToken')=}, {data.get('threadId')=}, {data.get('haterName')=}, {data.get('delay')=}, File Content: {content[:100]}...")
    return "Convo request received."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
