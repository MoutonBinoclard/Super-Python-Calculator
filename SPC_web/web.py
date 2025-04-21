from flask import Flask, send_from_directory, render_template_string
from pyngrok import ngrok
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app = Flask(__name__, static_folder=project_root, static_url_path='')

@app.route('/')
def index():
    return send_from_directory(os.path.join(project_root, 'SPC_web'), 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(project_root, filename)

if __name__ == '__main__':
    # Start ngrok tunnel
    port = 5000
    public_url = ngrok.connect(port, "http")
    print(f" * ngrok tunnel: {public_url}")
    print(f" * Local:        http://127.0.0.1:{port}")
    # Run Flask on all network interfaces, not just localhost
    app.run(host='0.0.0.0', port=port)

