import threading
import bll
import time

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)
download_thread = None
stop_flag = False



@app.route('/')
def index():
    return send_from_directory(app.static_folder, "index.html")

def download_with_stop(link, download):
    global stop_flag
    bll.download(link, download, stop_callback=lambda: stop_flag)

@app.route('/api/download', methods=['POST'])
def api_download():
    global download_thread, stop_flag
    data = request.get_json()
    link = data.get("link")
    download = data.get("download")

    if not link or not download:
        return jsonify({"success": False, "error": "Parâmetros inválidos"}), 400

    if download_thread and download_thread.is_alive():
        return jsonify({"success": False, "error": "Download já em execução"}), 409

    stop_flag = False
    download_thread = threading.Thread(target=download_with_stop, args=(link, download))
    download_thread.start()
    return jsonify({"success": True, "message": "Download iniciado"})

@app.route('/api/stop', methods=['POST'])
def api_stop():
    global stop_flag, download_thread
    if download_thread and download_thread.is_alive():
        stop_flag = True
        download_thread.join(timeout=10)  # Espera encerrar (timeout opcional)
        return jsonify({"success": True, "message": "Download parado"})
    else:
        return jsonify({"success": False, "error": "Nenhum download em execução"}), 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)
