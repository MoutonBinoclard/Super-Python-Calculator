from flask import Flask, send_from_directory, render_template_string
from pyngrok import ngrok
import os

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    # Serve the index.html file
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    # Serve static files (images, txt, css, etc.)
    return send_from_directory('.', filename)

if __name__ == '__main__':
    # Start ngrok tunnel
    port = 5000
    public_url = ngrok.connect(port, "http")
    print(f" * ngrok tunnel: {public_url}")
    print(f" * Local:        http://127.0.0.1:{port}")
    app.run(port=port)
