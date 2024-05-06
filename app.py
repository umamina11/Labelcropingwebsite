from flask import Flask, render_template, request, send_file
import os
import PyPDF2
import io

app = Flask(__name__)

def split_and_crop_pdf(input_pdf, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    cropped_pdfs = []

    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            # Calculate the width and height of the page
            width = page.mediabox.upper_right[0] - page.mediabox.lower_left[0]
            height = page.mediabox.upper_right[1] - page.mediabox.lower_left[1]

            # Define the amount of space you want to leave at the bottom and top
            space_to_leave_top = -62  # Adjust this value as needed
            space_to_leave_bottom = 10  # Adjust this value as needed

            # Set the crop box coordinates for the lower half of the page with a little space
            cropped_page = (page.cropbox.lower_left[0], page.cropbox.lower_left[1] + height / 2 - space_to_leave_top,
                            page.cropbox.lower_left[0] + width, page.cropbox.lower_left[1] + height - space_to_leave_bottom)
            page.cropbox.lower_left = (cropped_page[0], cropped_page[1])
            page.cropbox.upper_right = (cropped_page[2], cropped_page[3])

            writer = PyPDF2.PdfWriter()
            output_pdf = f"{output_folder}/page_{page_num + 1}.pdf"
            writer.add_page(page)
            
            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)
            
            cropped_pdfs.append(output_pdf)

    return cropped_pdfs

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        input_pdf = request.files['file']
        output_folder = request.form['output_folder']
        
        input_pdf_path = os.path.join('uploads', input_pdf.filename)
        input_pdf.save(input_pdf_path)
        
        cropped_pdfs = split_and_crop_pdf(input_pdf_path, output_folder)
        
        return render_template('download.html', pdfs=cropped_pdfs)
    return render_template('flipkart.html')

@app.route('/download/<path:pdf_path>')
def download_pdf(pdf_path):
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
