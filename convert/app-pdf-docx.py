import os
from flask import Flask, request, render_template, send_file
from pdf2docx import Converter
from datetime import datetime


app = Flask(__name__)

# Define the upload and converted file folders
UPLOAD_FOLDER = 'uploaded_files'
CONVERTED_FOLDER = 'converted_files'

# Define the full paths for the upload and converted folders
upload_path = os.path.join(os.getcwd(), UPLOAD_FOLDER)
converted_path = os.path.join(os.getcwd(), CONVERTED_FOLDER)

# Create the folders if they don't exist
os.makedirs(upload_path, exist_ok=True)
os.makedirs(converted_path, exist_ok=True)

def allowed_file(filename):
    # Only allowed .pdf extension
    allowed_extensions = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def secure_filename(filename):
    # Remove any unsafe characters from the filename
    return ''.join(c if c.isalnum() else '_' for c in filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return "No file part"

        file = request.files['file']

        # If the user does not select a file, the browser might submit an empty part without a filename
        if file.filename == '':
            return "No selected file"

        if file and allowed_file(file.filename):
            # Save the uploaded PDF file with a unique name
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            pdf_path = os.path.join(upload_path, f'{timestamp}_{filename}')
            file.save(pdf_path)

            # Convert the PDF to DOCX with a unique name
            docx_filename = f'{timestamp}_{filename}.docx'
            docx_path = os.path.join(converted_path, docx_filename)
            try:
                cv = Converter(pdf_path)
                cv.convert(docx_path)
                cv.close()
                result_msg = "Conversion successful! You can download the DOCX file below."
            except Exception as e:
                result_msg = f"Conversion failed: {e}"

            # Return the result page with the download link
            return render_template('result-pdf-docx.html', docx_filename=docx_filename, docx_file=docx_path)

    return render_template('upload-pdf-docx.html')

@app.route('/download/<path:docx_filename>')
def download_docx(docx_filename):
    docx_path = os.path.join(converted_path, docx_filename)
    return send_file(docx_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)