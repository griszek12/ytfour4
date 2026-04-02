from flask import Flask, request, send_file
import os
import uuid

app = Flask(__name__)

@app.route('/')
def home():
    return "Server działa!"

@app.route('/get')
def get_video():
    url = request.args.get('url')

    if not url:
        return "Brak URL", 400

    filename = f"{uuid.uuid4()}.mp4"

    # 🔥 yt-dlp z cookies + fallback + 240p
    cmd = f'yt-dlp --cookies cookies.txt --js-runtimes node -f "best[ext=mp4][height<=240]/best" -o "{filename}" "{url}"'

    result = os.system(cmd)

    # ❗ jeśli plik się nie pobrał
    if not os.path.exists(filename):
        return "Błąd pobierania (cookies wygasły albo blokada YouTube)", 500

    try:
        return send_file(filename, mimetype='video/mp4')
    except Exception as e:
        return f"Błąd wysyłania pliku: {str(e)}", 500

# 🔥 PORT dla Railway
port = int(os.environ.get("PORT", 3000))
app.run(host="0.0.0.0", port=port)
