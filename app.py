from flask import Flask, request, send_file
import os
import uuid

app = Flask(__name__)

@app.route('/get')
def get_video():
    url = request.args.get('url')
    filename = f"{uuid.uuid4()}.mp4"

    os.system(f'yt-dlp -f "mp4[height<=240]" -o "{filename}" "{url}"')

    return send_file(filename, mimetype='video/mp4')

app.run(host="0.0.0.0", port=3000)
