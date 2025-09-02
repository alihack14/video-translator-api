from flask import Flask, request, send_from_directory
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # هذا هو السطر المهم
    app.run(host="0.0.0.0", port=port)
#from moviepy.editor import VideoFileClip
import whisper
from deep_translator import GoogleTranslator

from flask import Flask, request, jsonify
import whisper

app = Flask(__name__)
model = whisper.load_model("base")

@app.route("/upload_with_translation", methods=["POST"])
def upload_with_translation():
    video = request.files["video"]
    target_lang = request.form["target_lang"]

    video_path = "temp_video.mp4"
    video.save(video_path)

    result = model.transcribe(video_path, language=target_lang)
    segments = result["segments"]  # يحتوي على text, start, end

    subtitles = [
        {"text": seg["text"], "start": seg["start"], "end": seg["end"]}
        for seg in segments
    ]

    return jsonify(subtitles)

model = whisper.load_model("base")

@app.route('/upload_with_translation', methods=['POST'])
def upload_with_translation():
    if 'video' not in request.files:
        return "No video file", 400

    video = request.files['video']
    video_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(video_path)

    result = model.transcribe(video_path)
    original_text = result['text']

    translated = GoogleTranslator(source='auto', target='ar').translate(original_text)

    # حفظ الترجمة في ملف نصي (اختياري)
    with open(os.path.join(TRANSLATED_FOLDER, 'translated.txt'), 'w', encoding='utf-8') as f:
        f.write(translated)

    return translated

@app.route('/translated/<path:filename>')
def serve_translated(filename):
    return send_from_directory(TRANSLATED_FOLDER, filename)
