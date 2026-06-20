import os
from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'default_search': 'ytsearch1:',
}

@app.route("/stream", methods=["GET"])
def stream_audio():
    q = request.args.get('q')
    if not q:
        return jsonify({"error": "Missing query"}), 400

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(q, download=False)
            if 'entries' in info and len(info['entries']) > 0:
                video_info = info['entries'][0]
            else:
                video_info = info

            stream_url = video_info.get('url')
            title = video_info.get('title', 'Unknown')

            if not stream_url:
                return jsonify({"error": "Stream not found"}), 404

            return jsonify({"title": title, "url": stream_url})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
