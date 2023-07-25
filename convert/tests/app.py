import os
from flask import Flask, request, send_file
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import PdfName
app = Flask(__name__)

# Configuration
app.config['UPLOADED_FILES_FOLDER'] = 'uploaded_files'
app.config['CONVERTED_FILES_FOLDER'] = 'converted_files'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def compress_pdf(input_path, output_path):
    pdf_reader = PdfReader(input_path)
    pdf_writer = PdfWriter()

    for page in pdf_reader.pages:
        # Reduce image/graph/chart resolution (dpi)
        if "/XObject" in page['/Resources']:
            xObject = page['/Resources']['/XObject'].get_object()
            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    xObject[obj].update({PdfName('/Filter'): PdfName('/DCTDecode')})

        # Compress text content (Optional: You may need to use other libraries for advanced text compression)

        pdf_writer.add_page(page)

    with open(output_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

@app.route('/', methods=['GET', 'POST'])
def compress_and_download():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']
        
        # Check if the file is selected
        if file.filename == '':
            return "No selected file"
        
        # Check if the file has the correct extension
        if file and allowed_file(file.filename):
            # Save the uploaded file
            uploaded_file_path = os.path.join(app.config['UPLOADED_FILES_FOLDER'], file.filename)
            file.save(uploaded_file_path)
            
            # Compress the PDF and save the converted file
            converted_file_path = os.path.join(app.config['CONVERTED_FILES_FOLDER'], 'compressed_' + file.filename)
            compress_pdf(uploaded_file_path, converted_file_path)
            
            # Provide the download link for the user
            return f'<a href="{converted_file_path}" download>Download Compressed PDF</a>'
        
        return "Invalid file format. Only PDF files are allowed."
    
    return '''
        <!doctype html>
        <title>PDF Compressor</title>
        <h1>Upload a PDF file to compress</h1>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Compress">
        </form>
    '''

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOADED_FILES_FOLDER']):
        os.makedirs(app.config['UPLOADED_FILES_FOLDER'])

    if not os.path.exists(app.config['CONVERTED_FILES_FOLDER']):
        os.makedirs(app.config['CONVERTED_FILES_FOLDER'])

    app.run()
