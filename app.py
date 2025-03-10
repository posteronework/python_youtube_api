# from flask import Flask, request, send_file, jsonify
# import yt_dlp
# import os
#
# app = Flask(__name__)
#
# DOWNLOAD_PATH = "downloads"
# os.makedirs(DOWNLOAD_PATH, exist_ok=True)
#
# @app.route("/download_audio", methods=["GET"])
# def download_audio():
#     youtube_url = request.args.get("url")
#     username = request.args.get("username")
#     password = request.args.get("password")
#
#     if not youtube_url or not username or not password:
#         return jsonify({"error": "URL, username, and password are required"}), 400
#
#     try:
#         # Настройки для yt-dlp с использованием логина и пароля
#         ydl_opts = {
#             "format": "bestaudio/best",
#             "outtmpl": f"{DOWNLOAD_PATH}/%(title)s.%(ext)s",
#             "username": username,  # Передаем логин напрямую
#             "password": password,  # Передаем пароль напрямую
#             "postprocessors": [{
#                 "key": "FFmpegExtractAudio",
#                 "preferredcodec": "wav",
#                 "preferredquality": "192"
#             }],
#             "quiet": True,  # Отключение лишнего вывода
#             "no_warnings": True,  # Отключение предупреждений
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
COOKIES_FILE = "cookies.txt"  # Временный файл для хранения куков

os.makedirs(DOWNLOAD_PATH, exist_ok=True)

def refresh_cookies(username, password):
    """
    Обновляет куки с использованием логина и пароля.
    """
    ydl_opts = {
        'username': username,
        'password': password,
        'cookiefile': COOKIES_FILE,  # Сохраняем куки в файл
        'quiet': True,  # Отключение вывода в консоль
        'no_warnings': True,  # Отключение предупреждений
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Используем любой URL для авторизации (нам не нужно скачивать видео)
            ydl.extract_info("https://www.youtube.com")
        print("Куки успешно обновлены.")
    except Exception as e:
        print(f"Ошибка при обновлении кук: {e}")
        raise

@app.route("/download_audio", methods=["GET"])
def download_audio():
    youtube_url = request.args.get("url")
    username = request.args.get("username")
    password = request.args.get("password")

    if not youtube_url or not username or not password:
        return jsonify({"error": "URL, username, and password are required"}), 400

    try:
        # Обновляем куки перед загрузкой аудио
        refresh_cookies(username, password)

        # Настройки для yt-dlp с использованием обновленных куков
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{DOWNLOAD_PATH}/%(title)s.%(ext)s",
            "cookiefile": COOKIES_FILE,  # Используем обновленные куки
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192"
            }],
            "quiet": True,  # Отключение лишнего вывода
            "no_warnings": True,  # Отключение предупреждений
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)