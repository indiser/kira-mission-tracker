import os
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder=None)

# Resolve the frontend directory relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, "templates")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")


@app.route("/")
def index():
    """Serve the main dashboard HTML."""
    return send_from_directory(TEMPLATES_DIR, "index.html")

@app.route("/login")
def login():
    """Serve the login page."""
    return send_from_directory(TEMPLATES_DIR, "login.html")

@app.route("/static/<path:filename>")
def static_files(filename):
    """Serve static frontend assets (CSS, JS, images)."""
    return send_from_directory(STATIC_DIR, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
