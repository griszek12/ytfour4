from flask import Flask, request, send_file, render_template_string, redirect
import os
import uuid
import subprocess

app = Flask(__name__)

# 🔹 Funkcja do poprawiania linku YouTube
def fix_youtube_url(url):
    if "youtu.be/" in url:
        video_id = url.split("/")[-1].split("?")[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return url

# 🌐 Strona główna
@app.route('/')
def home():
    return '''
    <html>
    <head>
        <title>YouTube 3G</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body style="font-family:sans-serif;text-align:center;margin-top:50px;">
        <h2>📺 YouTube dla iPhone 3G</h2>
        <form action="/get" method="get">
            <input name="url" placeholder="Wklej link YouTube"
            style="width:80%;padding:10px;font-size:16px;">
            <br><br>
            <button type="submit" style="padding:10px 20px;font-size:16px;">▶ Pobierz/Odtwórz 240p</button>
        </form>
        <br><br>
        <!-- 😈 Rickroll -->
        <a href="/get?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ">
            <button style="padding:8px 16px;">😈 Rickroll</button>
        </a>
        <p>⚡ Szybkie pobieranie • 240p • działa na iPhone 3G</p>
    </body>
    </html>
    '''

# 📥 Pobieranie/Odtwarzanie wideo
@app.route('/get')
def get_video():
    url = request.args.get('url')
    if not url:
        return "Brak URL", 400

    url = fix_youtube_url(url)
    filename = f"{uuid.uuid4()}.mp4"

    # ⚡ Pobieranie 240p MP4
    cmd = [
        "yt-dlp",
        "--no-playlist",
        "--retries", "3",
        "-f", "worst[ext=mp4][height<=240]/worst[ext=mp4]/worst",
        "-o", filename,
        url
    ]

    try:
        subprocess.run(cmd, check=True)
    except Exception as e:
        return f"Błąd pobierania: {str(e)}", 500

    if not os.path.exists(filename):
        return "Błąd pobierania pliku", 500

    # 🔹 Strona z odtwarzaczem
    html_player = f'''
    <html>
    <head>
        <title>Odtwarzanie YouTube 240p</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body style="text-align:center;font-family:sans-serif;margin-top:50px;">
        <h3>Odtwarzanie 240p</h3>
        <video controls autoplay style="width:90%;max-width:400px;">
            <source src="/stream/{filename}" type="video/mp4">
            Twój przeglądarka nie obsługuje HTML5 video.
        </video>
        <p><a href="/">🔙 Powrót</a></p>
    </body>
    </html>
    '''
    return html_player

# 🔹 Serwowanie pliku MP4 do odtwarzania
@app.route('/stream/<file>')
def stream_video(file):
    if not os.path.exists(file):
        return "Plik nie istnieje", 404
    return send_file(file, mimetype="video/mp4")

# 🔥 PORT
port = int(os.environ.get("PORT", 3000))
app.run(host="0.0.0.0", port=port)
