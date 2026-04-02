from flask import Flask, request, send_file
import os
import uuid
import subprocess
import re

app = Flask(__name__)

# 🔧 FIX LINKÓW
def fix_url(url):
    match = re.match(r'https?://youtu\.be/([^\?&]+)', url)
    if match:
        return f"https://www.youtube.com/watch?v={match.group(1)}"
    return url

# 🌐 STRONA
@app.route('/')
def home():
    return '''
    <html>
    <body style="text-align:center;margin-top:50px;font-family:sans-serif;">
        <h2>📺 YouTube 3G FIX</h2>

        <form action="/get">
            <input name="url" placeholder="Link YouTube" style="width:80%;padding:10px;">
            <br><br>
            <button>▶ Odtwórz</button>
        </form>

        <br>

        <a href="/get?url=https://youtu.be/dQw4w9WgXcQ">
            <button>😈 Rickroll</button>
        </a>
    </body>
    </html>
    '''

# 📥 POBIERANIE
@app.route('/get')
def get_video():
    url = request.args.get('url')
    if not url:
        return "Brak URL", 400

    url = fix_url(url)

    raw = f"{uuid.uuid4()}.raw"
    final = f"{uuid.uuid4()}.mp4"

    # 🔥 1. POBIERZ COKOLWIEK (NAWET WEBM)
    cmd_download = [
        "yt-dlp",
        "--no-playlist",
        "--retries", "5",
        "--sleep-interval", "2",
        "-o", raw,
        url
    ]

    try:
        subprocess.run(cmd_download, check=True)
    except:
        return "Błąd pobierania (429 lub blokada)", 500

    if not os.path.exists(raw):
        return "Nie pobrało pliku", 500

    # 🔥 2. KONWERSJA DO iPHONE 3G FORMAT
    cmd_convert = [
        "ffmpeg",
        "-i", raw,
        "-vf", "scale=320:-2",
        "-c:v", "libx264",
        "-profile:v", "baseline",
        "-level", "3.0",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "96k",
        final
    ]

    try:
        subprocess.run(cmd_convert, check=True)
    except:
        return "Błąd konwersji (ffmpeg?)", 500

    if not os.path.exists(final):
        return "Nie skonwertowało", 500

    # 🧹 sprzątanie
    try:
        os.remove(raw)
    except:
        pass

    # 🎬 WYŚLIJ DO SAFARI
    return send_file(final, mimetype="video/mp4", as_attachment=False)

# 🔥 PORT
port = int(os.environ.get("PORT", 3000))
app.run(host="0.0.0.0", port=port)
