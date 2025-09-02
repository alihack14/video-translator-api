import os
import tempfile
from flask import Flask, request, send_file
import whisper
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
model = whisper.load_model("tiny")

@app.route("/translate", methods=["POST"])
def translate():
    video = request.files["video"]
    lang = request.form.get("lang", os.getenv("DEFAULT_LANG", "ar"))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp:
        video.save(temp.name)
        result = model.transcribe(temp.name, language=lang)

    return result["text"]

@app.route("/subtitles", methods=["POST"])
def subtitles():
    video = request.files["video"]
    lang = request.form.get("lang", os.getenv("DEFAULT_LANG", "ar"))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp:
        video.save(temp.name)
        result = model.transcribe(temp.name, language=lang)

    subtitles = result["segments"]
    return {"subtitles": subtitles}

@app.route("/download_srt", methods=["POST"])
def download_srt():
    video = request.files["video"]
    lang = request.form.get("lang", os.getenv("DEFAULT_LANG", "ar"))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp:
        video.save(temp.name)
        result = model.transcribe(temp.name, language=lang)

    srt_lines = []
    for i, seg in enumerate(result["segments"]):
        start = format_timestamp(seg["start"])
        end = format_timestamp(seg["end"])
        text = seg["text"]
        srt_lines.append(f"{i+1}
{start} --> {end}
{text}

")

    srt_path = tempfile.NamedTemporaryFile(delete=False, suffix=".srt").name
    with open(srt_path, "w", encoding="utf-8") as f:
        f.writelines(srt_lines)

    return send_file(srt_path, as_attachment=True, download_name="translated.srt")

def format_timestamp(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)