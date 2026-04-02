from flask import Flask, request, send_file
import os
import uuid

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
        <a href="/get?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ">
            <button style="padding:8px 16px;">😈 Rickroll</button>
        </a>

        <p>⚡ Szybkie pobieranie • 240p • działa na iPhone 3G</p>

    </body>
    </html>
    '''

# 📥 POBIERANIE FILMU
@app.route('/get')
def get_video():
    url = request.args.get('url')

    if not url:
        return "Brak URL", 400

    filename = f"{uuid.uuid4()}.mp4"

    # ⚡ SZYBKI FORMAT 240p
    cmd = f'yt-dlp --cookies cookies.txt --no-playlist --retries 3 -f "worst[ext=mp4][height<=240]/worst[ext=mp4]/worst" -o "{filename}" "{url}"'

    os.system(cmd)

    # ❗ sprawdzenie czy plik istnieje
    if not os.path.exists(filename):
        return "Błąd pobierania (spróbuj inny film lub odśwież cookies)", 500

    try:
        return send_file(filename, mimetype='video/mp4')
    except Exception as e:
        return f"Błąd wysyłania pliku: {str(e)}", 500

# 🔥 PORT (Render / Railway)
port = int(os.environ.get("PORT", 3000))
app.run(host="0.0.0.0", port=port)
