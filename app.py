from flask import Flask
import os

app = Flask(__name__)  # Fix the double underscores here

@app.route("/")
def home():
    return "Hello, Flask is running on Heroku!"

if __name__ == "__main__":  # Fix the double underscores here too
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
