from flask import Flask, request, render_template, send_file
from moviepy.editor import VideoFileClip
import whisper
import os
import json

from utils.cleaner import clean_text
from utils.translator import translate_text
from utils.subtitle_burner import burn_subtitles
from utils.encoder import reencode_video

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
TRANSLATED_FOLDER = "static/translated_videos"
RECORDS_PATH = "data/records.json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSLATED_FOLDER, exist_ok=True)
os.makedirs("data", exist_ok=True)

def format_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

@app.route("/", methods=["GET", "POST"])
def index():
    translated_video = None
    if request.method == "POST":
        video = request.files["video"]
        lang = request.form.get("lang", "ar")
        video_path = os.path.join(UPLOAD_FOLDER, video.filename)
        video.save(video_path)

        # ترميز الفيديو لضمان التوافق
        encoded_video_path = reencode_video(video_path, UPLOAD_FOLDER)

        # استخراج الصوت
        clip = VideoFileClip(encoded_video_path)
        audio_path = encoded_video_path + ".wav"
        clip.audio.write_audiofile(audio_path)

        # تحويل الصوت إلى نص
        model = whisper.load_model("large")
        result = model.transcribe(audio_path, language=None)

        # إنشاء ملف SRT
        srt_path = encoded_video_path + ".srt"
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, segment in enumerate(result["segments"], start=1):
                start = format_timestamp(segment["start"])
                end = format_timestamp(segment["end"])
                text = clean_text(segment["text"])
                translated = translate_text(text, lang)
                f.write(f"{i}\n{start} --> {end}\n{translated}\n\n")

        # دمج الترجمة داخل الفيديو
        translated_video_path = burn_subtitles(encoded_video_path, srt_path, TRANSLATED_FOLDER)
        translated_video = os.path.basename(translated_video_path)

        # حفظ السجل
        record = {
            "original": video.filename,
            "translated": translated_video,
            "srt": os.path.basename(srt_path),
            "lang": lang,
            "status": "done"
        }
        records = []
        if os.path.exists(RECORDS_PATH):
            with open(RECORDS_PATH, "r", encoding="utf-8") as f:
                records = json.load(f)
        records.append(record)
        with open(RECORDS_PATH, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)

    return render_template("index.html", video=translated_video)

@app.route("/dashboard")
def dashboard():
    records = []
    if os.path.exists(RECORDS_PATH):
        with open(RECORDS_PATH, "r", encoding="utf-8") as f:
            records = json.load(f)
    return render_template("dashboard.html", records=records)

@app.route("/download/<file>")
def download(file):
    return send_file(os.path.join(UPLOAD_FOLDER, file), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=10000)