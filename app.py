from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import http.cookiejar

app = Flask(__name__)

DOWNLOAD_PATH = "downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

def get_cookie_jar():
    """
    Создает и возвращает объект http.cookiejar.CookieJar для хранения куков.
    """
    return http.cookiejar.CookieJar()

@app.route("/download_audio", methods=["GET"])
def download_audio():
    youtube_url = request.args.get("url")
    username = request.args.get("username")
    password = request.args.get("password")

    if not youtube_url or not username or not password:
        return jsonify({"error": "URL, username, and password are required"}), 400

    try:
        # Создаем объект для хранения куков
        cookie_jar = get_cookie_jar()

        # Настройки для yt-dlp с использованием логина, пароля и куков
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{DOWNLOAD_PATH}/%(title)s.%(ext)s",
            "username": username,  # Передаем логин напрямую
            "password": password,  # Передаем пароль напрямую
            "cookiejar": cookie_jar,  # Используем http.cookiejar для хранения куков
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192"
            }],
            "quiet": True,
            "no_warnings": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)