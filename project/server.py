import threading
import bll

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

download_thread = None
stop_event = threading.Event()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, "index.html")

def download_with_stop(link, download):
    bll.download(link, download, stop_callback=lambda: stop_event.is_set())

@app.route('/api/download', methods=['POST'])
def api_download():
    global download_thread, stop_event
    data = request.get_json()
    link = data.get("link")
    download = data.get("download")

    if not link or not download:
        return jsonify({"success": False, "error": "Parâmetros inválidos"}), 400

    if download_thread and download_thread.is_alive():
        return jsonify({"success": False, "error": "Download já em execução"}), 409

    stop_event.clear()
    download_thread = threading.Thread(target=download_with_stop, args=(link, download))
    download_thread.start()
    return jsonify({"success": True, "message": "Download iniciado"})

@app.route('/api/stop', methods=['POST'])
def api_stop():
    global stop_event, download_thread
    if download_thread and download_thread.is_alive():
        stop_event.set()
        download_thread.join(timeout=10)
        return jsonify({"success": True, "message": "Download parado"})
    else:
        return jsonify({"success": False, "error": "Nenhum download em execução"}), 400

@app.route('/api/status', methods=['GET'])
def api_status():
    global download_thread
    is_running = download_thread.is_alive() if download_thread else False
    return jsonify({"running": is_running})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
