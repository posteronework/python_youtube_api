# from flask import Flask, request, send_file, jsonify
# import yt_dlp
# import os
#
# app = Flask(__name__)
#
# DOWNLOAD_PATH = "downloads"
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
import re

app = Flask(__name__)

# Папка для загрузок
DOWNLOAD_PATH = "downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# Файл cookies (если нужен вход в YouTube)
COOKIES_FILE = "cookies.txt"  # Экспортируй из браузера (см. инструкции)

# Функция для очистки имени файла
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

@app.route("/download_audio", methods=["GET"])
def download_audio():
    youtube_url = request.args.get("url")

    if not youtube_url:
        return jsonify({"error": "URL is required"}), 400

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{DOWNLOAD_PATH}/%(title)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192"
            }],
            "cookies": COOKIES_FILE if os.path.exists(COOKIES_FILE) else None,
            "noprogress": True,  # Убираем прогресс из логов
            "quiet": True,  # Отключаем лишние логи
            "throttledratelimit": 5000000,  # 5MB/s (обход 429 Too Many Requests)
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            title = sanitize_filename(info.get("title", "audio"))
            filename = os.path.join(DOWNLOAD_PATH, f"{title}.wav")

        # Отправляем файл и удаляем его после отправки
        response = send_file(filename, as_attachment=True)
        os.remove(filename)
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
