# from flask import Flask, request, send_file, jsonify
# import yt_dlp
# import os
#
# app = Flask(__name__)
#
# DOWNLOAD_PATH = "downloads"
# COOKIES_FILE = "cookies.txt"
#
# os.makedirs(DOWNLOAD_PATH, exist_ok=True)
#
#
# @app.route("/download_audio", methods=["GET"])
# def download_audio():
#     youtube_url = request.args.get("url")
#
#     if not youtube_url:
#         return jsonify({"error": "URL is required"}), 400
#
#     try:
#         ydl_opts = {
#             "format": "bestaudio/best",
#             "outtmpl": f"{DOWNLOAD_PATH}/%(title)s.%(ext)s",
#             "cookiefile": COOKIES_FILE,
#             "postprocessors": [{
#                 "key": "FFmpegExtractAudio",
#                 "preferredcodec": "wav",
#                 "preferredquality": "192"
#             }]
#         }
#
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(youtube_url, download=True)
#             filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
#
#         return send_file(filename, as_attachment=True)
#
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#
#
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5001, debug=True)
from flask import Flask, request, send_file, jsonify
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_PATH = "downloads"
COOKIES_FILE = "cookies.txt"  # Файл, в который будут сохраняться куки

os.makedirs(DOWNLOAD_PATH, exist_ok=True)

@app.route("/upload_cookies", methods=["POST"])
def upload_cookies():
    if 'cookies' not in request.files:
        return jsonify({"error": "Файл с куками не найден"}), 400

    file = request.files['cookies']
    file.save(COOKIES_FILE)
    return jsonify({"message": "Файл с куками успешно загружен"}), 200

@app.route("/download_audio", methods=["GET"])
def download_audio():
    youtube_url = request.args.get("url")

    if not youtube_url:
        return jsonify({"error": "URL обязателен"}), 400

    try:
        # Параметры для скачивания аудио
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{DOWNLOAD_PATH}/%(title)s.%(ext)s",
            "cookiefile": COOKIES_FILE,  # Используем загруженные куки
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192"
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
