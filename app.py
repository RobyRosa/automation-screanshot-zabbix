import os
import subprocess
import pytz
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv
# from whatsapp import send_to_whatsapp

app = Flask(__name__)

ASIA_JAKARTA_TZ = pytz.timezone('Asia/Jakarta')
# Path penyimpanan screenshot
SCREENSHOT_DIR = "./screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

WHATSAPP_API_URL = os.getenv('WHATSAPP_API_URL')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

@app.route('/capture', methods=['POST'])
def capture_graph():
    try:
        data = request.json
        graph_url = data.get('graph_url')  # Full URL grafik Grafana
        group_name = data.get('group_name', "Infrastructure")
        caption = data.get('caption', "Test Send Graph CPU DBsehati")

        if not graph_url:
            return jsonify({"error": "graph_url is required"}), 400

        # Timestamp dengan zona waktu Asia/Jakarta
        timestamp = datetime.now(ASIA_JAKARTA_TZ).strftime("%Y%m%d_%H")

        # Nama file output screenshot
        output_file = os.path.join(SCREENSHOT_DIR, f"sehati_{timestamp}.png")

        # Jalankan Puppeteer untuk mengambil screenshot
        subprocess.run([
            "node", "capture.js",
            graph_url, output_file
        ], check=True)

        with open(output_file, 'rb') as file:
            files = {'file': (os.path.basename(output_file), file, 'image/png')}
            data = {
                'group_name': group_name,
                'caption': caption
            }
            headers = {
                'Cookie': f'token={AUTH_TOKEN}'
            }
            response = requests.post(WHATSAPP_API_URL, data=data, files=files, headers=headers)

        return jsonify({
            "message": "Screenshot captured and sent to WhatsApp",
            "file": output_file,
            "whatsapp_response": response.json() if response.status_code == 200 else response.text
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
