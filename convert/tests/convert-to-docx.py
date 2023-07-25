from pdf2docx import Converter

def convert_pdf_to_docx(pdf_path, docx_path):
    try:
        # Initialize the converter
        cv = Converter(pdf_path)

        # Convert the PDF to DOCX
        cv.convert(docx_path)

        # Close the converter
        cv.close()

        print("Conversion successful!")
    except Exception as e:
        print(f"Conversion failed: {e}")

if __name__ == "__main__":
    # Replace 'input_file.pdf' with the path of your input PDF file
    input_pdf_path = "ACM_IGDTUW.pdf"

    # Replace 'output_file.docx' with the desired path for the output DOCX file
    output_docx_path = "output_file.docx"

    # Call the conversion function
    convert_pdf_to_docx(input_pdf_path, output_docx_path)
