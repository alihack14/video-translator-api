from flask import Flask, request, send_from_directory
import os
from moviepy.editor import VideoFileClip
import whisper
from deep_translator import GoogleTranslator

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
TRANSLATED_FOLDER = 'translated'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSLATED_FOLDER, exist_ok=True)

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
