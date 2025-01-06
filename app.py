from flask import Flask, jsonify
import random
import string
import datetime

app = Flask(__name__)

# Generate random IP
def generate_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

# Generate random username
def generate_username():
    return f"user_{random.randint(1000, 9999)}"

# Generate random password
def generate_password():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(10))

# Calculate expiration date (30 days from now)
def get_expiration_date():
    return (datetime.datetime.now() + datetime.timedelta(days=30)).strftime('%Y-%m-%d')

@app.route('/generate_rdp', methods=['GET'])
def generate_rdp():
    rdp_details = {
        "ip_address": generate_ip(),
        "username": generate_username(),
        "password": generate_password(),
        "expiration_date": get_expiration_date(),
        "port": 3389  # Default RDP port
    }
    return jsonify(rdp_details)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
