

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file





from flask import send_from_directory
import tempfile
import PyPDF2

import os
import qrcode

from PyPDF2 import PdfMerger
from werkzeug.utils import secure_filename
import re
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

UPLOAD_FOLDER = 'skusort'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_sku(text):
    sku_pattern = r'\b\d{6}\b'
    skus = re.findall(sku_pattern, text)
    skus = [int(sku) for sku in skus]
    return skus

def process_pdf(file_path):
    sku_dict = defaultdict(list)
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text = page.extractText()
            skus = extract_sku(text)
            for sku in skus:
                sku_dict[sku].append(page)
    return sku_dict

def create_sorted_pdf(sku_dict):
    output_pdf = PyPDF2.PdfWriter()
    for sku, pages in sorted(sku_dict.items()):
        for page in pages:
            output_pdf.addPage(page)
    return output_pdf

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            sku_dict = process_pdf(file_path)
            sorted_pdf = create_sorted_pdf(sku_dict)
            sorted_folder = 'sorted_pdfs'
            os.makedirs(sorted_folder, exist_ok=True)
            sorted_filename = os.path.join(sorted_folder, 'sorted_labels.pdf')
            with open(sorted_filename, 'wb') as output_file:
                sorted_pdf.write(output_file)
            return 'Labels sorted successfully! <a href="/download">Download sorted labels</a>'
    return render_template('upload.html')

@app.route('/download')
def download_file():
    sorted_filename = 'sorted_pdfs/sorted_labels.pdf'
    return redirect(url_for('static', filename=sorted_filename), code=301)

if __name__ == '__main__':
    app.run(debug=True)