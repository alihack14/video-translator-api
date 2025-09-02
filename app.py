import os
import tempfile
from flask import Flask, request, send_file, jsonify
import whisper

app = Flask(__name__)
model = whisper.load_model("tiny")  # نموذج خفيف لتقليل استهلاك الذاكرة

@app.route("/translate", methods=["POST"])
def translate():
    video = request.files.get("video")
    lang = request.form.get("lang", "ar")

    if not video:
        return "No video uploaded", 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp:
        video.save(temp.name)
        result = model.transcribe(temp.name, language=lang)

    return result["text"]

@app.route("/subtitles", methods=["POST"])
def subtitles():
    video = request.files.get("video")
    lang = request.form.get("lang", "ar")

    if not video:
        return "No video uploaded", 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp:
        video.save(temp.name)
        result = model.transcribe(temp.name, language=lang)

    segments = result.get("segments", [])
    subtitles = [
        {
            "start": round(seg["start"], 2),
            "end": round(seg["end"], 2),
            "text": seg["text"]
        }
        for seg in segments
    ]

    return jsonify({"subtitles": subtitles})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # حل مشكلة Render
    app.run(host="0.0.0.0", port=port)
