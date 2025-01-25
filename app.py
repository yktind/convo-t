from flask import Flask, request, render_template, jsonify
import time
import requests

app = Flask(__name__)

# Home route to display the form
@app.route('/')
def home():
    return '''
    <h1>Facebook Automation</h1>
    <form action="/send_message" method="POST" enctype="multipart/form-data">
        <label for="token">Enter Facebook Token:</label><br>
        <input type="text" name="token" required><br><br>
        
        <label for="target_id">Enter Target User ID:</label><br>
        <input type="text" name="target_id" required><br><br>
        
        <label for="delay">Enter Delay (seconds):</label><br>
        <input type="number" name="delay" min="1" required><br><br>
        
        <label for="file">Upload Text File:</label><br>
        <input type="file" name="file" accept=".txt" required><br><br>
        
        <button type="submit">Send Messages</button>
    </form>
    '''

# Route to process the message sending
@app.route('/send_message', methods=['POST'])
def send_message():
    token = request.form['token']
    target_id = request.form['target_id']
    delay = int(request.form['delay'])
    file = request.files['file']
    
    if not file:
        return "No file uploaded.", 400
    
    # Read messages from the uploaded text file
    messages = file.read().decode('utf-8').splitlines()
    
    for message in messages:
        url = f"https://graph.facebook.com/v16.0/{target_id}/messages"
        payload = {
            "recipient": {"id": target_id},
            "message": {"text": message}
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Send message using POST request
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print(f"Message sent: {message}")
        else:
            print(f"Failed to send message: {response.json()}")
        
        # Delay between messages
        time.sleep(delay)
    
    return "Messages sent successfully!"

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
