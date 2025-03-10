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
COOKIES_FILE = "cookies.txt"

os.makedirs(DOWNLOAD_PATH, exist_ok=True)

def clear_cookies(cookies_file=COOKIES_FILE):
    try:
        if os.path.exists(cookies_file):
            os.remove(cookies_file)
            print(f"Файл {cookies_file} очищен.")
        else:
            print(f"Файл {cookies_file} не найден.")
    except Exception as e:
        print(f"Ошибка при очистке файла куков: {e}")

def get_fresh_cookies(cookies_file=COOKIES_FILE):
    try:
        # Extract cookies from the browser and save to a file
        ydl_opts = {
            'cookiesfrombrowser': ('chrome',),  # Extract from Chrome
            'cookies': cookies_file
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info("https://www.youtube.com", download=False)
        print(f"Свежие куки сохранены в {cookies_file}")
    except Exception as e:
        print(f"Ошибка при получении свежих куков: {e}")

@app.route("/download_audio", methods=["GET"])
def download_audio():
    youtube_url = request.args.get("url")

    if not youtube_url:
        return jsonify({"error": "URL is required"}), 400

    try:
        clear_cookies(COOKIES_FILE)  # Очистить старые куки
        get_fresh_cookies(COOKIES_FILE)  # Получить новые куки

        # Параметры для скачивания аудио
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{DOWNLOAD_PATH}/%(title)s.%(ext)s",
            "cookiefile": COOKIES_FILE,  # Используем обновленные куки
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
