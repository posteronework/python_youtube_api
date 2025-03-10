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
import browser_cookie3

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
        # Извлеките куки из браузера
        cookies = browser_cookie3.chrome(domain_name='youtube.com')

        # Сохраните куки в файл в формате Netscape
        with open(cookies_file, "w") as f:
            f.write("# HTTP Cookie File\n")
            for cookie in cookies:
                f.write(f"{cookie.domain}\tTRUE\t{cookie.path}\tFALSE\t{int(cookie.expires)}\t{cookie.name}\t{cookie.value}\n")

        print(f"Свежие куки сохранены в {cookies_file}")
    except Exception as e:
        print(f"Ошибка при получении свежих куков: {e}")

@app.route("/upload_cookies", methods=["POST"])
def upload_cookies():
    clear_cookies()
    get_fresh_cookies()
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
