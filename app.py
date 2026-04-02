from flask import Flask, request, send_file
import os
import uuid
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

# 🌐 FUNKCJA NAPRAWY LINKU
def fix_youtube_url(url):
    url = url.strip()
    if "youtu.be/" in url:
        # Skrócony link youtu.be/lvGMEdcTxYc?si=...
        parsed = urlparse(url)
        video_id = parsed.path.lstrip('/')  # lvGMEdcTxYc
        return f"https://www.youtube.com/watch?v={video_id}"
    elif "youtube.com/watch" in url:
        # Pełny link, ale możemy oczyścić parametry
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        video_id = qs.get('v', [''])[0]
        return f"https://www.youtube.com/watch?v={video_id}" if video_id else url
    return url

# 🌐 STRONA GŁÓWNA
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
        
        <form action="/get">
            <input name="url" placeholder="Wklej link YouTube"
            style="width:80%;padding:10px;font-size:16px;">
            
            <br><br>
            
            <button type="submit" style="padding:10px 20px;font-size:16px;">
                📥 Pobierz MP4
            </button>
        </form>

        <br><br>

        <a href="/get?url=https://youtu.be/dQw4w9WgXcQ">
            <button>😈 Rickroll</button>
        </a>

        <p>⚡ Pobieranie MP4 • działa na iPhone 3G</p>

    </body>
    </html>
    '''

# 📥 POBIERANIE
@app.route('/get')
def get_video():
    url = request.args.get('url')

    if not url:
        return "Brak URL", 400

    url = fix_youtube_url(url)  # 🔧 Napraw link

    filename = f"{uuid.uuid4()}.mp4"

    cmd = f'yt-dlp --cookies cookies.txt --no-playlist --retries 3 -f "worst[ext=mp4][height<=240]/worst[ext=mp4]/worst" -o "{filename}" "{url}"'
    os.system(cmd)

    if not os.path.exists(filename):
        return "Błąd pobierania", 500

    return send_file(
        filename,
        mimetype='video/mp4',
        as_attachment=True,
        download_name="video.mp4"
    )

# 🔥 PORT
port = int(os.environ.get("PORT", 3000))
app.run(host="0.0.0.0", port=port)
