from flask import Flask, request
from werkzeug.utils import secure_filename
import os
from flask import Flask, request, jsonify, Response
import whisper
import tempfile

app = Flask(__name__)
model = whisper.load_model("tiny")

@app.route('/')
def home():
    return "الخدمة تعمل بنجاح من Flask 🎉"

@app.route('/upload_with_translation', methods=['POST'])
def upload_with_translation():
    video = request.files.get('video')
    target_lang = request.form.get('target_lang', 'ar')
    format_type = request.form.get('format', 'json')  # 'json' أو 'srt'

    if not video:
        return "لم يتم إرسال فيديو", 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        video.save(temp_video.name)

        result = model.transcribe(temp_video.name, language=target_lang)
        segments = result["segments"]

        if format_type == "srt":
            srt_output = ""
            for i, seg in enumerate(segments, start=1):
                start = format_timestamp(seg["start"])
                end = format_timestamp(seg["end"])
                text = seg["text"].strip()
                srt_output += f"{i}\n{start} --> {end}\n{text}\n\n"
            return Response(srt_output, mimetype="text/plain")

        else:  # JSON
            subtitles = [
                {"text": seg["text"], "start": seg["start"], "end": seg["end"]}
                for seg in segments
            ]
            return jsonify(subtitles)

def format_timestamp(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"


@app.route('/')
def home():
    return "الخدمة تعمل بنجاح من Flask 🎉"

@app.route('/upload_with_translation', methods=['POST'])
def upload_with_translation():
    video = request.files.get('video')
    target_lang = request.form.get('target_lang', 'ar')

    if not video:
        return "لم يتم إرسال فيديو", 400

    filename = secure_filename(video.filename)
    save_path = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)
    video.save(save_path)

    # هنا تقدر تضيف كود Whisper أو أي ترجمة
    return f"تم استلام الفيديو: {filename} بلغة: {target_lang}"

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
