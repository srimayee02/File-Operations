import os
import PyPDF2
from gtts import gTTS
from flask import Flask, render_template, request, send_file
from datetime import datetime

app = Flask(__name__)

def get_current_datetime_string():
    now = datetime.now()
    return now.strftime("%Y%m%d%H%M%S")

@app.route('/', methods=['GET', 'POST'])
def convert_pdf_to_audio():
    if request.method == 'POST' and 'pdf_file' in request.files:
        pdf_file = request.files['pdf_file']
        if pdf_file:
            filename = pdf_file.filename.split('.')[0]
            pdf_filename = f"uploads/{filename}_{get_current_datetime_string()}.pdf"
            pdf_file.save(pdf_filename)

            # Convert PDF to text and audio
            pdf_text = extract_text_from_pdf(pdf_filename)
            audio_file = convert_text_to_audio(pdf_text, filename)

            # Provide the option to download the audio file
            return render_template('result-pdf-audio.html', audio_file=audio_file)

    return render_template('upload-pdf-audio.html')

def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_text += page.extract_text()
    return pdf_text

def convert_text_to_audio(text, filename):
    tts = gTTS(text, lang='en')
    audio_filename = f"converted/{filename}_{get_current_datetime_string()}.mp3"
    tts.save(audio_filename)
    return audio_filename

@app.route('/download/<path:audio_file>')
def download_audio(audio_file):
    return send_file(audio_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
