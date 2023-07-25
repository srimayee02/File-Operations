from flask import Flask, request, render_template, send_file
import os
from PyPDF2 import PdfReader, PdfWriter

app = Flask(__name__)

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
            # Save the uploaded PDF file temporarily
            pdf_path = "temp-compress.pdf"
            file.save(pdf_path)

            # Compress the PDF: only minor compression occurs with sample pdf
            compressed_pdf_path = "compressed_file.pdf"
            compress_pdf(pdf_path, compressed_pdf_path)

            
            return render_template('result-compress.html', compressed_pdf_path=compressed_pdf_path)

    return render_template('upload-compress.html')

@app.route('/download', methods=['GET'])
def download_file():
    compressed_pdf_path = "compressed_file.pdf"
    return send_file(compressed_pdf_path, as_attachment=True)

def allowed_file(filename):
    # Allowed file extension 
    allowed_extensions = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def compress_pdf(input_path, output_path):
    with open(input_path, "rb") as file:
        pdf_reader = PdfReader(file)
        pdf_writer = PdfWriter()

        for page in pdf_reader.pages:
            page.compress_content_streams()
            pdf_writer.add_page(page)
        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)


if __name__ == "__main__":
    app.run(debug=True)