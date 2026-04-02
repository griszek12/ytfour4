from flask import Flask, request, send_file, redirect
import os
import uuid
import re

app = Flask(__name__)

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
                ▶ Pobierz 240p
            </button>
        </form>

        <br><br>

        <!-- 😈 RICKROLL BUTTON -->
        <a href="/get?url=https://youtu.be/dQw4w9WgXcQ">
            <button style="padding:8px 16px;">😈 Rickroll</button>
        </a>

        <p>⚡ Szybkie pobieranie • 240p • działa na iPhone 3G</p>

    </body>
    </html>
    '''

# 🔧 FUNKCJA POPRAWIAJĄCA LINKI
def fix_youtube_url(url):
    # youtu.be -> youtube.com/watch?v=
    match = re.match(r'https?://youtu\.be/([^\?&]+)', url)
    if match:
        return f"https://www.youtube.com/watch?v={match.group(1)}"
    return url

# 📥 POBIERANIE FILMU
@app.route('/get')
def get_video():
    url = request.args.get('url')
    if not url:
        return "Brak URL", 400

    url = fix_youtube_url(url)
    filename = f"{uuid.uuid4()}.mp4"

    # ⚡ SZYBKI FORMAT 240p
    cmd = f'yt-dlp --no-playlist --retries 3 -f "worst[height<=240]" --recode-video mp4 --postprocessor-args "-vcodec libx264 -profile:v baseline -level 3.0 -acodec aac -ar 44100" -o "{filename}" "{url}"'
    os.system(cmd)

    # ❗ sprawdzenie czy plik istnieje
    if not os.path.exists(filename):
        return "Błąd pobierania (spróbuj inny film)", 500

    try:
        # 🔥 SERVE DIRECTLY FOR BROWSER
        return send_file(filename, mimetype='video/mp4', as_attachment=False)
    except Exception as e:
        return f"Błąd wysyłania pliku: {str(e)}", 500

# 🔥 PORT (Render / Railway)
port = int(os.environ.get("PORT", 3000))
app.run(host="0.0.0.0", port=port)
