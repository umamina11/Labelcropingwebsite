

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file





from flask import send_from_directory
import tempfile
import PyPDF2

import os
import qrcode

from PyPDF2 import PdfMerger

from collections import defaultdict


app = Flask(__name__)


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/amazon')
def amazon():
    return render_template('amazon.html')

@app.route('/flipkart')
def flipkart():
    return render_template('flipkart.html')

@app.route('/meesho')
def meesho():
    return render_template('meesho.html')

@app.route('/glowroad')
def glowroad():
    return render_template('glowroad.html')

@app.route('/merge')
def merge():
    return render_template('merge.html')

@app.route('/QRCode')
def QRCode():
    return render_template('QRCode.html')


@app.route('/fouroption')
def fouroption():
    return render_template('fouroption.html')



## split and crop the labels

def split_and_crop_pdf(input_pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(input_pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            width = page.mediabox.upper_right[0] - page.mediabox.lower_left[0]
            height = page.mediabox.upper_right[1] - page.mediabox.lower_left[1]
            space_to_leave_top = -62
            space_to_leave_bottom = 10
            cropped_page = (page.cropbox.lower_left[0], page.cropbox.lower_left[1] + height / 2 - space_to_leave_top,
                            page.cropbox.lower_left[0] + width, page.cropbox.lower_left[1] + height - space_to_leave_bottom)
            page.cropbox.lower_left = (cropped_page[0], cropped_page[1])
            page.cropbox.upper_right = (cropped_page[2], cropped_page[3])

            writer = PyPDF2.PdfWriter()
            output_pdf = os.path.join(output_folder, f"page_{page_num + 1}.pdf")
            writer.add_page(page)

            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)
            print(f"Cropped page {page_num + 1} saved as {output_pdf}")

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            # Save uploaded file to a temporary location
            _, temp_file_path = tempfile.mkstemp(suffix='.pdf')
            file.save(temp_file_path)
            output_folder = 'output'
            split_and_crop_pdf(temp_file_path, output_folder)
            return redirect(url_for('download_files'))

@app.route('/download')
def download_files():
    directory = 'output'
    return render_template('download.html', files=os.listdir(directory))

@app.route('/download/<path:filename>')
def download_file(filename):
    directory = 'output'
    return send_from_directory(directory, filename)


#merge pdf

@app.route('/merge_pdfs', methods=['POST'])
def merge_pdfs():
    uploaded_files = request.files.getlist("files")
    
    merger = PdfMerger()
    for file in uploaded_files:
        merger.append(file)
    
    merged_filename = 'merged.pdf'
    merger.write(merged_filename)
    merger.close()
    
    return send_file(merged_filename, as_attachment=True)


## QR Code Generator
@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.form['data']
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image temporarily
    img_path = "temp_qr.png"
    img.save(img_path)

    # Send the file for download
    return send_file(img_path, as_attachment=True)

###
####
#####
######
#
def split_and_crop_pdf(input_pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(input_pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            # Crop logic here
            
            # Example crop logic for demonstration, adjust according to your needs
            cropped_page = page.crop(0, 0, 100, 100)  # Crop example: (left, top, right, bottom)

            writer = PyPDF2.PdfWriter()
            output_pdf = os.path.join(output_folder, f"page_{page_num + 1}.pdf")
            writer.add_page(cropped_page)

            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)
            print(f"Cropped page {page_num + 1} saved as {output_pdf}")

# Function to sort PDF pages by quantity, courier, and SKU
def sort_pdf_pages(output_folder, sort_by):
    sorted_files = []
    # Sort logic based on the chosen sort option
    if sort_by == 'quantity':
        # Sort by quantity logic
        pass
    elif sort_by == 'courier':
        # Sort by courier logic
        pass
    elif sort_by == 'SKU':
        # Sort by SKU logic
        pass
    return sorted_files

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            _, temp_file_path = tempfile.mkstemp(suffix='.pdf')
            file.save(temp_file_path)
            output_folder = 'output'
            split_and_crop_pdf(temp_file_path, output_folder)
            # Redirect to page for choosing sorting option
            return redirect(url_for('choose_sorting_option'))

@app.route('/choose_sorting_option')
def choose_sorting_option():
    return render_template('choose_sorting_option.html')

@app.route('/sort_and_download', methods=['POST'])
def sort_and_download():
    sort_by = request.form.get('sort_by')
    output_folder = 'output'
    sorted_files = sort_pdf_pages(output_folder, sort_by)
    # Merge sorted PDFs into one
    merger = PdfMerger()
    for file_name in sorted_files:
        file_path = os.path.join(output_folder, file_name)
        merger.append(file_path)
    merged_filename = 'sorted_merged.pdf'
    merger.write(merged_filename)
    merger.close()
    # Download the merged and sorted PDF
    return send_file(merged_filename, as_attachment=True)

# Add route for downloading individual sorted PDFs if needed

if __name__ == '__main__':
    app.run(debug=True)

