from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Navi Badmash</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
<style>
label{ color: white; }
.file{ height: 30px; }
body{
background-image: url('https://i.ibb.co/fFqG2rr/Picsart-24-07-11-17-16-03-306.jpg');
background-size: cover;
background-repeat: no-repeat;
color: white;
}
.container{
max-width: 350px;
height: 600px;
border-radius: 20px;
padding: 20px;
box-shadow: 0 0 15px white;
border: none;
resize: none;
}
.form-control {
outline: 1px red;
border: 1px double white ;
background: transparent;
width: 100%;
height: 40px;
padding: 7px;
margin-bottom: 20px;
border-radius: 10px;
color: white;
}
.header{
text-align: center;
padding-bottom: 20px;
}
.btn-submit{
width: 100%;
margin-top: 10px;
}
.footer{
text-align: center;
margin-top: 20px;
color: #888;
}
.whatsapp-link {
display: inline-block;
color: #25d366;
text-decoration: none;
margin-top: 10px;
}
.whatsapp-link i {
margin-right: 5px;
}
</style>
</head>
<body>
<header class="header mt-4">
<h1 class="mt-3">倫Navi Badmash倫 </h1>
</header>
<div class="container text-center">
<form action="/" method="post" enctype="multipart/form-data">
<div class="mb-3">
<label for="accessToken">Attach Token File:</label>
<input type="file" class="form-control" id="accessToken" name="accessToken" accept=".txt" required>
</div>
<div class="mb-3">
<label for="threadId">Enter Convo/Inbox ID:</label>
<input type="text" class="form-control" id="threadId" name="threadId" required>
</div>
<div class="mb-3">
<label for="kidx">Enter Hater Name:</label>
<input type="text" class="form-control" id="kidx" name="kidx" required>
</div>
<div class="mb-3">
<label for="txtFile">Select Your Notepad File:</label>
<input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
</div>
<div class="mb-3">
<label for="time">Speed in Seconds:</label>
<input type="number" class="form-control" id="time" name="time" required>
</div>
<button type="submit" class="btn btn-primary btn-submit">Submit Your Details</button>
</form>
<footer class="footer">
<p>&copy; 2025 ★ 𝘼𝙡𝙡 𝙍𝙞𝙜𝙝𝙩𝙨 𝙍𝙚𝙨𝙚𝙧𝙫𝙚𝙙 𝘽𝙮 Navi Badmash ★</p>
<p>FB FIGHTER<a href="https://www.facebook">ᴄʟɪᴄᴋ ʜᴇʀᴇ ғᴏʀ ғᴀᴄᴀʙᴏᴏᴋ</a></p>
<div class="mb-3">
<a href="https://wa.me/+91" class="whatsapp-link">
<i class="fab fa-whatsapp"></i> Chat on WhatsApp
</a>
</div>
</footer>
</div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        thread_id = request.form.get('threadId')
        kidx = request.form.get('kidx')
        speed = request.form.get('time')

        access_token_file = request.files.get('accessToken')
        txt_file = request.files.get('txtFile')

        if access_token_file and txt_file:
            access_token_path = os.path.join(app.config['UPLOAD_FOLDER'], access_token_file.filename)
            txt_file_path = os.path.join(app.config['UPLOAD_FOLDER'], txt_file.filename)

            access_token_file.save(access_token_path)
            txt_file.save(txt_file_path)

            return f"<h2 style='color:white;'>Received:<br>Thread ID: {thread_id}<br>Hater: {kidx}<br>Speed: {speed} sec<br>Files Uploaded.</h2>"

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
  
