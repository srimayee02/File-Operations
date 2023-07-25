import os
from flask import Flask, request, render_template, send_file
import pandas as pd
import tabula
from openpyxl import Workbook

app = Flask(__name__)

# Define the upload and converted file folders
UPLOAD_FOLDER = 'uploaded_files'
CONVERTED_FOLDER = 'converted'

# Define the full paths for the upload and converted folders
upload_path = os.path.join(os.getcwd(), UPLOAD_FOLDER)
converted_path = os.path.join(os.getcwd(), CONVERTED_FOLDER)

# Create the folders if they don't exist
os.makedirs(upload_path, exist_ok=True)
os.makedirs(converted_path, exist_ok=True)

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
            pdf_path = os.path.join(upload_path, secure_filename(file.filename))
            file.save(pdf_path)

            # Convert the PDF to XLSX with a unique name
            xlsx_filename = f"{os.path.splitext(file.filename)[0]}.xlsx"
            xlsx_path = os.path.join(converted_path, secure_filename(xlsx_filename))
            try:
                # Use tabula to extract the tables from the PDF
                df = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)

                # Save the extracted tables to an XLSX file
                save_df_to_excel(df, xlsx_path)

                result_msg = "Conversion successful! You can download the XLSX file below."
            except Exception as e:
                result_msg = f"Conversion failed: {e}"

            # Return the result page with the download link
            return render_template('result-pdf-xlsx.html', result_msg=result_msg, xlsx_filename=xlsx_filename)

    return render_template('upload-pdf-xlsx.html')

@app.route('/download/<path:xlsx_filename>')
def download_xlsx(xlsx_filename):
    xlsx_path = os.path.join(converted_path, xlsx_filename)
    return send_file(xlsx_path, as_attachment=True)

def allowed_file(filename):
    # Only allowed .pdf extension
    allowed_extensions = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def secure_filename(filename):
    # Remove any unsafe characters from the filename
    return ''.join(c if c.isalnum() or c == '.' else '_' for c in filename)

def save_df_to_excel(df, output_path):
    # Save DataFrame to Excel using openpyxl engine
    book = Workbook()
    sheet = book.active

    for row in pd.dataframe_to_rows(df, index=False, header=True):
        sheet.append(row)

    book.save(output_path)
if __name__ == "__main__":
    app.run(debug=True)
