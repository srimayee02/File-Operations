from fpdf import FPDF
from flask import Flask, render_template, send_file, request
from datetime import datetime

app = Flask(__name__)

# Function to get the current date and time as a formatted string
def get_current_datetime_string():
    now = datetime.now()
    return now.strftime("%Y%m%d%H%M%S")

@app.route('/', methods=['GET', 'POST'])
def convert_txt_to_pdf():
    if request.method == 'POST':
        # Save the uploaded TXT file to the 'uploads' directory
        txt_file = request.files['txt_file']
        if txt_file:
            filename = f"uploads/{get_current_datetime_string()}_input.txt"
            txt_file.save(filename)

            # Convert TXT to PDF
            output_pdf = f"converted/{get_current_datetime_string()}_output.pdf"
            pdf = FPDF()
            pdf.add_page() 
            pdf.set_font("Arial", size = 15) 

            with open(filename, "r") as f:
                for x in f:
                    pdf.cell(200, 10, txt=x, ln=1, align='C') 
            pdf.output(output_pdf) 

            # Provide the option to download the converted PDF file
            return download_pdf_txt(output_pdf)

    return render_template('upload-txt-pdf.html')

@app.route('/download/<path:pdf_file>')
def download_pdf_txt(pdf_file):
    return send_file(pdf_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)