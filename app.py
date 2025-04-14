from flask import Flask, request, render_template_string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Messenger Bot</title>
</head>
<body>
    <h2>Facebook Messenger Auto Sender</h2>
    <form method="POST">
        <label>Email:</label><br>
        <input type="email" name="email" required><br><br>

        <label>Password:</label><br>
        <input type="password" name="password" required><br><br>

        <label>Target Name:</label><br>
        <input type="text" name="target_name" required><br><br>

        <label>Message:</label><br>
        <textarea name="message_text" required></textarea><br><br>

        <button type="submit">Send Message</button>
    </form>

    {% if status %}
    <p>{{ status }}</p>
    {% endif %}
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    status = ""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        target_name = request.form["target_name"]
        message_text = request.form["message_text"]

        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
            driver.get("https://www.messenger.com/")
            time.sleep(3)

            driver.find_element(By.ID, "email").send_keys(email)
            pass_input = driver.find_element(By.ID, "pass")
            pass_input.send_keys(password)
            pass_input.send_keys(Keys.RETURN)

            time.sleep(5)

            search_box = driver.find_element(By.XPATH, '//input[@type="search"]')
            search_box.send_keys(target_name)
            time.sleep(3)
            driver.find_element(By.XPATH, f"//span[text()='{target_name}']").click()
            time.sleep(3)

            msg_box = driver.find_element(By.XPATH, '//div[@aria-label="Type a message…"]')
            msg_box.send_keys(message_text)
            msg_box.send_keys(Keys.RETURN)

            status = "✅ Message Sent Successfully!"
        except Exception as e:
            status = f"❌ Error: {str(e)}"
        finally:
            time.sleep(2)
            driver.quit()

    return render_template_string(HTML_TEMPLATE, status=status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
