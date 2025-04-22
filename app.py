from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Mr. Drip MLB Home Run Alerts is Live</h1>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render's required port binding
    app.run(debug=False, host="0.0.0.0", port=port)
