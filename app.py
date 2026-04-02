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

    # 🔥 lepsza komenda (fallback + prostsza)
    cmd = f'yt-dlp -f "best[ext=mp4][height<=240]/best" -o "{filename}" "{url}"'

    result = os.system(cmd)

    # ❗ sprawdzamy czy plik istnieje
    if not os.path.exists(filename):
        return "Błąd pobierania (YouTube blokuje lub brak formatu)", 500

    return send_file(filename, mimetype='video/mp4')

port = int(os.environ.get("PORT", 3000))
app.run(host="0.0.0.0", port=port)
