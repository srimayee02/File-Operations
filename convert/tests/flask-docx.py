from flask import Flask, request, render_template, send_file
from pdf2docx import Converter

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
            pdf_path = "temp.pdf"
            file.save(pdf_path)

            # Convert the PDF to DOCX
            docx_path = "output_file.docx"
            try:
                
                cv = Converter(pdf_path)
                
                cv.convert(docx_path)
                
                cv.close()
                result_msg = "Conversion successful! You can download the DOCX file below."
            except Exception as e:
                result_msg = f"Conversion failed: {e}"

            # Return the result page with the download link
            return render_template('result-docx.html', result_msg=result_msg, docx_path=docx_path)

    return render_template('upload-docx.html')

@app.route('/download', methods=['GET'])
def download_file():
    docx_path = "output_file.docx"
    return send_file(docx_path, as_attachment=True)

def allowed_file(filename):
    #Only allowed .pdf extension
    allowed_extensions = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

if __name__ == "__main__":
    app.run(debug=True)
