import requests

# URL Backend API WhatsApp
WHATSAPP_API_URL = "http://contohhh:8000/send-message"  # Ganti dengan URL API Anda

def send_to_whatsapp(file_path):
    """Mengirim file screenshot ke API WhatsApp."""
    try:
        with open(file_path, "rb") as file:
            files = {"file": file}
            data = {
                "message": "Grafik terbaru dari Zabbix.",
                "to": "6281234567890"  # Nomor tujuan, ganti sesuai kebutuhan
            }
            response = requests.post(WHATSAPP_API_URL, data=data, files=files)
        
        if response.status_code == 200:
            return {"message": "Screenshot berhasil dikirim ke WhatsApp"}
        else:
            raise RuntimeError(f"Gagal mengirim pesan WhatsApp: {response.text}")
    except Exception as e:
        raise RuntimeError(f"Error saat mengirim ke WhatsApp: {e}")
