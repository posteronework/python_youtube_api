# from flask import Flask, request, send_file
# from pytube import YouTube
# from pydub import AudioSegment
# import os
#
# app = Flask(__name__)
#
# @app.route('/download_audio', methods=['GET'])
# def download_audio():
#     video_url = request.args.get('url')
#     if not video_url:
#         return "URL видео не предоставлен", 400
#
#     try:
#         # Создаем объект YouTube
#         yt = YouTube(video_url)
#
#         # Выбираем аудиопоток
#         audio_stream = yt.streams.filter(only_audio=True).first()
#
#         # Скачиваем в MP3
#         temp_mp3 = "audio.mp3"
#         audio_stream.download(filename=temp_mp3)
#
#         # Конвертируем в M4A
#         temp_m4a = "audio.m4a"
#         audio = AudioSegment.from_file(temp_mp3, format="mp3")
#         audio.export(temp_m4a, format="ipod")  # iPod = M4A (AAC)
#
#         # Удаляем MP3 (оставляем только M4A)
#         os.remove(temp_mp3)
#
#         return send_file(temp_m4a, as_attachment=True)
#
#     except Exception as e:
#         return f"Ошибка: {str(e)}", 500
#
#     finally:
#         # Удаляем файл после отправки
#         if os.path.exists(temp_m4a):
#             os.remove(temp_m4a)
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001)

from flask import Flask, request, send_file
from pytube import YouTube
from pydub import AudioSegment
import os

app = Flask(__name__)

@app.route('/download_audio', methods=['GET'])
def download_audio():
    video_url = request.args.get('url')
    if not video_url:
        return "URL видео не предоставлен", 400

    try:
        # Создаем объект YouTube
        yt = YouTube(video_url)

        # Выбираем аудиопоток
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Скачиваем в MP4 (AAC)
        temp_mp4 = "audio.mp4"
        audio_stream.download(filename=temp_mp4)

        # Конвертируем в WAV
        temp_wav = "audio.wav"
        audio = AudioSegment.from_file(temp_mp4, format="mp4")
        audio.export(temp_wav, format="wav", parameters=["-ar", "16000", "-ac", "1"])  # 16 кГц, моно

        # Удаляем временный MP4
        os.remove(temp_mp4)

        return send_file(temp_wav, as_attachment=True)

    except Exception as e:
        return f"Ошибка: {str(e)}", 500

    finally:
        # Удаляем файл после отправки
        if os.path.exists(temp_wav):
            os.remove(temp_wav)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)