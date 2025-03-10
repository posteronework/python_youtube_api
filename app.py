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

# Функция для получения свежих кук через логин и пароль
def get_fresh_cookies(youtube_url, username, password, cookies_file=COOKIES_FILE):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{DOWNLOAD_PATH}/%(title)s.%(ext)s",
        "cookiefile": cookies_file,  # Сохраняем куки в файл
        "username": username,
        "password": password,
        "quiet": True,  # Убираем лишние выводы
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Выполняем извлечение информации (без загрузки самого контента), чтобы получить куки
        ydl.extract_info(youtube_url, download=False)

    print(f"Куки обновлены и сохранены в {cookies_file}")

# Очистка файла куков перед их обновлением
def clear_cookies(cookies_file=COOKIES_FILE):
    try:
        if os.path.exists(cookies_file):
            os.remove(cookies_file)
            print(f"Файл {cookies_file} очищен.")
        else:
            print(f"Файл {cookies_file} не найден.")
    except Exception as e:
        print(f"Ошибка при очистке файла куков: {e}")


@app.route("/download_audio", methods=["GET"])
def download_audio():
    youtube_url = request.args.get("url")
    username = request.args.get("username")
    password = request.args.get("password")

    if not youtube_url:
        return jsonify({"error": "URL is required"}), 400

    if not username or not password:
        return jsonify({"error": "Username and password are required for authorization"}), 400

    try:
        clear_cookies(COOKIES_FILE)  # Очистить старые куки
        get_fresh_cookies(youtube_url, username, password)  # Получить новые куки

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
