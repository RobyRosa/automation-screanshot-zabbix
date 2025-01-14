import os
import subprocess
import pytz
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# Path penyimpanan screenshot
SCREENSHOT_DIR = "./screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Zona waktu Asia/Jakarta
ASIA_JAKARTA_TZ = pytz.timezone('Asia/Jakarta')

@app.route('/capture', methods=['POST'])
def capture_graph():
    try:
        data = request.json
        graph_url = data.get('graph_url')  # Full URL grafik Grafana

        if not graph_url:
            return jsonify({"error": "graph_url is required"}), 400
        
        timestamp = datetime.now(ASIA_JAKARTA_TZ).strftime("%Y%m%d_%H")

        # Nama file output screenshot
        output_file = os.path.join(SCREENSHOT_DIR, f"sehati_{timestamp}.png")

        # Jalankan Puppeteer untuk mengambil screenshotd
        subprocess.run([
            "node", "capture.js",
            graph_url, output_file
        ], check=True)

        return jsonify({"message": "Screenshot captured", "file": output_file}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
