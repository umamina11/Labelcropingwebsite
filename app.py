from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/flipkart')
def flipkart():
    return render_template('flipkart.html', platform='Flipkart')

@app.route('/amazon')
def amazon():
    return render_template('amazon.html', platform='Amazon')

@app.route('/meesho')
def meesho():
    return render_template('meesho.html', platform='Meesho')

@app.route('/glassdoor')
def glassdoor():
    return render_template('glassdoor.html', platform='Glassdoor')




from flask import Flask, render_template, request, redirect, url_for
from PyPDF2 import PdfFileReader, PdfFileWriter

app = Flask(__name__)

# Function to crop each page of the PDF into half
def crop_pdf_half(pdf_file):
    pdf_reader = PdfFileReader(pdf_file)
    pdf_writer = PdfFileWriter()

    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        media_box = page.mediaBox
        media_box.lowerLeft = (media_box.getLowerLeft_x(), media_box.getLowerLeft_y())
        media_box.upperRight = (media_box.getUpperRight_x() / 2, media_box.getUpperRight_y())
        pdf_writer.addPage(page)

    return pdf_writer

# Function to split all pages of the PDF into halves
def split_pdf_half(pdf_file):
    pdf_reader = PdfFileReader(pdf_file)
    pdf_writer = PdfFileWriter()

    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        media_box = page.mediaBox
        width = media_box.getUpperRight_x() - media_box.getLowerLeft_x()
        height = media_box.getUpperRight_y() - media_box.getLowerLeft_y()

        half_width = width / 2
        half_height = height / 2

        for x in range(2):
            for y in range(2):
                new_page = pdf_writer.addBlankPage(half_width, half_height)
                new_page.mergeTranslatedPage(page, -x * half_width, -y * half_height)

    return pdf_writer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'pdf_file' not in request.files:
        return redirect(request.url)

    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return redirect(request.url)

    if pdf_file:
        # Crop each page into half
        cropped_pdf_half = crop_pdf_half(pdf_file)
        cropped_half_filename = 'cropped_half.pdf'
        with open(cropped_half_filename, 'wb') as output_pdf:
            cropped_pdf_half.write(output_pdf)

        # Split all pages into halves
        split_pdf = split_pdf_half(pdf_file)
        split_half_filename = 'split_half.pdf'
        with open(split_half_filename, 'wb') as output_pdf:
            split_pdf.write(output_pdf)

        return render_template('result.html', 
                                cropped_half_filename=cropped_half_filename,
                                split_half_filename=split_half_filename)

@app.route('/flipkart')
def flipkart():
    return render_template('flipkart.html')

@app.route('/amazon')
def amazon():
    return render_template('amazon.html')

@app.route('/meesho')
def meesho():
    return render_template('meesho.html')

@app.route('/glassdoor')
def glassdoor():
    return render_template('glassdoor.html')

if __name__ == '__main__':
    app.run(debug=True)
