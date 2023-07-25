from flask import Flask, render_template, request, send_file
from docx2pdf import convert
import os
from datetime import datetime

app = Flask(__name__)

# Function to get the current date and time as a formatted string
def get_current_datetime_string():
    now = datetime.now()
    return now.strftime("%Y%m%d%H%M%S")

@app.route('/', methods=['GET', 'POST'])
def convert_docx_to_pdf():
    if request.method == 'POST':
        # Save the uploaded DOCX file to the 'uploads' directory
        docx_file = request.files['docx_file']
        if docx_file:
            filename = f"uploads/{get_current_datetime_string()}_input.docx"
            docx_file.save(filename)

            # Convert DOCX to PDF
            output_pdf = f"converted/{get_current_datetime_string()}_output.pdf"
            convert(filename, output_pdf)

            # Provide the option to download the converted PDF file
            return render_template('result-docx-pdf.html', pdf_file=output_pdf)

    return render_template('upload-docx-pdf.html')

@app.route('/download/<path:pdf_file>')
def download_pdf(pdf_file):
    return send_file(pdf_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
