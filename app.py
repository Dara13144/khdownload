"""
app.py - Flask API for remote video downloads
"""

from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Folder where videos will be saved (must be writable)
DOWNLOAD_DIR = "/path/to/downloads"  # Change this to a real path on your server/phone

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    # Call the downloader script
    try:
        result = subprocess.run(
            ['python', 'downloader.py', url, DOWNLOAD_DIR],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes max
        )
        if result.returncode == 0:
            # Success: the script prints "SUCCESS:filename"
            output = result.stdout.strip()
            if output.startswith("SUCCESS:"):
                filename = output[8:]
                return jsonify({'message': 'Download successful', 'file': filename})
            else:
                return jsonify({'message': 'Download started, but unknown output', 'output': output})
        else:
            return jsonify({'error': result.stderr}), 500
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Download timed out'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run on all interfaces, port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
