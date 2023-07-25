from flask import render_template, send_file, Flask, request
from datetime import datetime
import win32com
import win32com.client
import os

win32com.CoInitialize()

app = Flask(__name__)

def get_current_datetime_string():
    now = datetime.now()
    return now.strftime("%Y%m%d%H%M%S")


@app.route('/', methods=['GET', 'POST'])
def convert_pptx_to_pdf():
    if request.method == 'POST':
        # Save the uploaded DOCX file to the 'uploads' directory
        pptx_file = request.files['pptx_file']
        if pptx_file:
            filename = f"uploads/{get_current_datetime_string()}_input.pptx"
            pptx_file.save(filename)

            # Convert DOCX to PDF
            output_pdf = f"converted/{get_current_datetime_string()}_output.pdf"
            powerpoint = win32com.client.DispatchEx("Powerpoint.Application")
            deck = powerpoint.Presentations.Open(os.path.abspath(pptx_file.filename))
            deck.SaveAs(os.path.abspath(output_pdf), 32)  # 32 is the constant value for PDF format
            deck.Close()
            powerpoint.Quit()

            # Provide the option to download the converted PDF file
            return render_template('result-pptx-pdf.html', pdf_file=output_pdf)

    return render_template('upload-pptx-pdf.html')


@app.route('/download/<path:pdf_file>')
def download_pdf_pptx(pdf_file):
    return send_file(pdf_file, as_attachment=True)

@app.teardown_appcontext
def teardown_comtypes(exception):
    win32com.CoUninitialize()

if __name__ == '__main__':
    app.run(debug=True)
