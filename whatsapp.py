import requests

# URL Backend API WhatsApp
WHATSAPP_API_URL = "http://192.168.91.163:7000/api/kirimGambarKeGrup"
def send_to_whatsapp(file_path, group_name="Infrastructure", caption="Grafik terbaru"):
    """
    Mengirim file screenshot ke API WhatsApp.

    Args:
        file_path (str): Path file gambar yang akan dikirim.
        group_name (str): Nama grup WhatsApp tujuan.
        caption (str): Caption untuk gambar.

    Returns:
        dict: Respon dari API WhatsApp jika berhasil.

    Raises:
        RuntimeError: Jika terjadi kesalahan saat mengirim pesan.
    """
    try:
        with open(file_path, "rb") as file:
            files = {"file": file}
            data = {
                "group_name": group_name,
                "caption": caption,
            }
            headers = {
                "Cookie": "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNzM2ODI1OTgzfQ.cphQTEAqFKey0bOZdaACxxDmv2dLf12VK0qGtoBwDDQ"
            }

            response = requests.post(WHATSAPP_API_URL, data=data, files=files, headers=headers)

        if response.status_code == 200:
            return {"message": "Screenshot berhasil dikirim ke WhatsApp", "response_data": response.json()}
        else:
            raise RuntimeError(f"Gagal mengirim pesan WhatsApp: {response.text}")
    except Exception as e:
        raise RuntimeError(f"Error saat mengirim ke WhatsApp: {e}")
