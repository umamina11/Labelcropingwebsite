

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file


from flask import send_from_directory
import tempfile
import PyPDF2
import io
import os
import qrcode

from PyPDF2 import PdfMerger
from werkzeug.utils import secure_filename
import re
from collections import defaultdict

import tempfile
from fpdf import FPDF
from PyPDF2 import PdfFileReader
import pandas as pd

app = Flask(__name__)


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
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


'''

def extract_skus_from_pdf(pdf_file):
    skus = []
    reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text = page.extract_text()
        sku_matches = re.findall(r'\b[0-9A-Za-z]{6}\b', text)  # Adjust the regex pattern as per your SKU format
        skus.extend(sku_matches)
    return skus



def sort_skus(skus):
    sorted_skus = sorted(skus)
    return sorted_skus


def create_sorted_pdf(skus):
    pdf_writer = PyPDF2.PdfWriter()
    buffer = io.BytesIO()

    for sku in skus:
        pdf_writer.add_blank_page(width=612, height=792)

    pdf_writer.write(buffer)
    buffer.seek(0)

    return buffer



@app.route('/sort')
def sort():
    return render_template('sort.html')

from flask import send_file

@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('sort.html', error='No file part')
        file = request.files['file']
        if file.filename == '':
            return render_template('sort.html', error='No selected file')
        if file:
            _, temp_file_path = tempfile.mkstemp(suffix='.pdf')
            file.save(temp_file_path)
            skus = extract_skus_from_pdf(temp_file_path)
            sorted_skus = sort_skus(skus)
            sorted_pdf = create_sorted_pdf(sorted_skus)
            return send_file(
                sorted_pdf,
                mimetype='application/pdf',
                as_attachment=True,
                download_name='sorted_skus.pdf'  # Specify the filename here
            )



if __name__ == "__main__":
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
    '''
    
    
'''
    ## sort 
def extract_skus_from_pdf(pdf_file):
    skus = []
    reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text = page.extract_text()
        sku_matches = re.findall(r'\b[0-9A-Za-z]{6}\b', text)
        skus.extend(sku_matches)
    return skus

def sort_skus(skus):
    sorted_skus = sorted(skus)
    return sorted_skus

def create_sorted_pdf(skus, pdf_file):
    pdf_writer = PyPDF2.PdfWriter()

    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for sku in skus:
            try:
                page_num = int(sku) - 1
            except ValueError:
                print(f"Invalid SKU: {sku}. Skipping...")
                continue

            if 0 <= page_num < len(reader.pages):
                page = reader.pages[page_num]
                pdf_writer.add_page(page)
            else:
                print("Invalid page number:", page_num)

    buffer = io.BytesIO()
    pdf_writer.write(buffer)
    buffer.seek(0)

    return buffer

@app.route('/sort')
def sort():
    return render_template('sort.html')

@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('sort.html', error='No file part')
        file = request.files['file']
        if file.filename == '':
            return render_template('sort.html', error='No selected file')
        if file:
            _, temp_file_path = tempfile.mkstemp(suffix='.pdf')
            file.save(temp_file_path)
            skus = extract_skus_from_pdf(temp_file_path)
            sorted_skus = sort_skus(skus)
            sorted_pdf = create_sorted_pdf(sorted_skus, temp_file_path)
            return send_file(
                sorted_pdf,
                mimetype='application/pdf',
                as_attachment=True,
                download_name='sorted_skus.pdf'
            )

@app.route('/download_sorted')
def download_sorted():
    return render_template('sorted.html')

if __name__ == "__main__":
    app.run(debug=True)
    
'''
def extract_data_from_pdf(pdf_path):
    reader = PdfFileReader(open(pdf_path, 'rb'))
    data = []
    for page_num in range(reader.numPages):
        text = reader.getPage(page_num).extract_text()
        lines = text.split('\n')
        # Parsing logic to extract data based on the document structure
        for line in lines:
            if "SKU" in line:
                sku = line.split(" ")[1]
            if "Qty" in line:
                qty = line.split(" ")[1]
            if "Courier" in line:
                courier = line.split(" ")[1]
        data.append({"SKU": sku, "Qty": qty, "Courier": courier})
    return pd.DataFrame(data)

@app.route('/other')
def other():
    return render_template('other.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        data = extract_data_from_pdf(file_path)
        sort_options = request.form.getlist('options')
        if sort_options:
            data = data.sort_values(by=sort_options)
        
        sorted_file_path = file_path.replace('.pdf', '_sorted.pdf')
        # Save sorted data to a new PDF (this part requires further implementation)
        
        return send_from_directory(app.config['UPLOAD_FOLDER'], os.path.basename(sorted_file_path))
    return 'Invalid file format'

if __name__ == '__main__':
    app.run(debug=True)