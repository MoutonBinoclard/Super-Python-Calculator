from flask import Flask, send_from_directory, render_template_string, url_for, Response, abort
from pyngrok import ngrok
import os
import json
import sys
import mimetypes


def get_exe_dir():
    if getattr(sys, 'frozen', False):
        # If running as a PyInstaller EXE, use the temp folder
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

# New: real runtime dir (where the EXE lives) for dynamic content like "exports"
def get_runtime_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# Add: helper to disable client-side caching
def _add_no_cache_headers(resp: Response) -> Response:
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp

project_root = os.path.dirname(os.path.abspath(__file__))
    
def read_entry_from_settings(settings_path, entry_name):
    with open(settings_path, 'r', encoding='utf-8') as f:
        settings = json.load(f)
        return settings.get(entry_name, None)

# Create Flask app
app = Flask(__name__, static_folder=project_root, static_url_path='')

@app.route('/')
def index():
    try:
        title_web = read_entry_from_settings("settings.json", "title_web")

        # Read index.html content
        index_path = os.path.join(get_exe_dir(), 'index.html')
        with open(index_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Replace the <h1>...</h1> with the dynamic title
        html_content = html_content.replace(
            '<h1>SPC V7 - Live leaderboard</h1>',
            f'<h1>{title_web}</h1>'
        )

        return render_template_string(html_content)
    except Exception as e:
        return f"Error serving index.html: {str(e)}"

@app.route('/exports/<path:filename>')
def serve_exports(filename):
    # Serve dynamic files from the real runtime directory, not the PyInstaller temp dir
    exports_dir = os.path.join(get_runtime_dir(), 'exports')
    try:
        # Sanitize path to prevent traversal
        base = os.path.abspath(exports_dir)
        requested = os.path.abspath(os.path.join(exports_dir, filename))
        if not (requested == base or requested.startswith(base + os.sep)):
            abort(404)
        if not os.path.isfile(requested):
            abort(404)

        # Read and return file with strong no-cache headers
        with open(requested, 'rb') as f:
            data = f.read()
        mimetype = mimetypes.guess_type(requested)[0] or 'application/octet-stream'
        resp = Response(data, mimetype=mimetype)
        return _add_no_cache_headers(resp)
    except Exception as e:
        return f"Error serving exports file: {str(e)}"

@app.route('/<path:filename>')
def serve_static(filename):
    try:
        return send_from_directory(project_root, filename)
    except Exception as e:
        return f"Error serving static file: {str(e)}"

if __name__ == '__main__':
    port = 5000

    auth_token = read_entry_from_settings("settings.json", "auth_token")
    if auth_token:
        ngrok.set_auth_token(auth_token)
        public_url = ngrok.connect(port, "http")
        print(f" * ngrok tunnel: {public_url}")
    
    print(f" * Local:        http://127.0.0.1:{port}")
    print(f" * Project root: {project_root}")
    
    # Run Flask on all network interfaces, not just localhost
    app.run(host='0.0.0.0', port=port)