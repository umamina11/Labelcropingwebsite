# Label Cropping Website

The provided Flask application serves as a simple web-based tool for processing PDF files. Here's a description of its main functionalities:

1. Homepage and Navigation: The application features a homepage with links to different sections, such as "Amazon", "Flipkart", "Meesho", and "Glassdoor".
These links provide navigation to different pages within the application.

2. File Upload: On the homepage, there is a form where users can upload a PDF file. Users can select a PDF file from their local system and specify a name for the output folder where the processed files will be saved.

3. PDF Processing: After uploading a PDF file, the application processes the file by splitting each page into upper and lower halves. It uses the PyPDF2 library to perform this task. The upper and
lower halves of each page are saved as separate PDF files in the specified output folder.

4. File Download: Once the PDF file is processed, the application provides a list of processed files on a separate page. Users can see a list of processed PDF files along with download links.
Clicking on a file name allows users to download the corresponding processed PDF file.

5. Additional Pages The application includes links to additional pages related to various topics (e.g., Amazon, Flipkart, etc.). These pages are placeholders
and can be expanded or customized to provide more content or functionality.

Overall, the application provides a user-friendly interface for uploading PDF files, processing them, and downloading the processed files. It can be further extended and customized to meet specific requirements or 
integrated into larger web applications.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Functionalities](#functionalities)
- [Contact](#contact)

## Installation

Tools and Technologies used: <br>
Python<br>
HTML<br>
CSS<br>
Flask<br>
Visual Studio 2019<br>


1. Install Python: If you don't have Python installed on your system, download and install it from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/). Make sure to add Python to your system's PATH during installation.

2. Install Flask: Flask is a Python web framework used for building web applications. You can install Flask using pip, the Python package installer. Open your command-line interface and run the following command:
   ```
   pip install Flask
   ```

3. Install PyPDF2: PyPDF2 is a library for working with PDF files in Python. Install it using pip:
   ```
   pip install PyPDF2
   ```

Once you've installed Python, Flask, and PyPDF2, you're ready to run the provided Flask application. Save the code in a file (e.g., `app.py`) and run it using the Python interpreter:

```
python app.py
```

This command will start the Flask development server, and you can access the application in your web browser at `http://127.0.0.1:5000/`.


## Modules 
Flask: Flask is a web framework for Python used to build web applications. It is used to define routes, handle HTTP requests, and render HTML templates.
PyPDF2: PyPDF2 is a library for working with PDF files in Python. It is used in the code to read, manipulate, and write PDF files. Specifically, it is used to split each page 
of the uploaded PDF file into upper and lower halves.
os: The os module provides a way to interact with the operating system. In the code, it is used to perform operations related to file and directory manipulation, such as creating directories (os.makedirs) 
and listing directory contents (os.listdir).
tempfile: The tempfile module provides functions to create temporary files and directories. In the code, it is used to create a temporary file path for storing the uploaded PDF file before processing.
render_template: render_template is a function provided by Flask for rendering HTML templates. It is used to render HTML templates that are served to the client.
request: The request module in Flask provides access to incoming request data such as form data, file uploads, and request headers. It is used to handle form submissions and file uploads in the code.
redirect: The redirect function in Flask is used to redirect the client to a different URL. It is used in the code to redirect the client to a different page after form submission or file processing.
url_for: The url_for function in Flask is used to generate URLs for endpoint functions. It is used in the code to generate URLs for redirecting the client and creating download links.
send_from_directory: The send_from_directory function in Flask is used to send files from a specified directory to the client. It is used in the code to serve processed PDF files for download.

## Functionalities 
Rendering HTML Templates: The application defines routes for rendering different HTML templates (index, amazon, flipkart, meesho, glassdoor). These routes are accessed via 
their respective URLs and serve HTML content to the client.
File Upload: The application allows users to upload PDF files via a form submission. The form contains an input field for selecting a PDF file (<input type="file">) and an input field for 
specifying an output folder name. Upon submission, the file is uploaded to the server.
PDF Processing: After uploading a PDF file, the application processes the file using the split_and_crop_pdf function. This function splits each page of the PDF file into upper and lower halves and 
saves them as separate PDF files in an output folder. The processing is done using the PyPDF2 library.
File Download: Once the PDF file is processed, the application allows users to download the processed files. It provides a list of processed files in the output folder and generates download links 
for each file. Clicking on a download link allows the user to download the corresponding processed PDF file.

## Usage

On terminal first run command <br>
pip install PyPDF2
pip install flask<br>
And then run the file using the command <br>
python app.py(file name)

Sure, here's how you can use the provided Flask application:

1. Starting the Application: Save the provided code in a Python file (e.g., `app.py`). Open a terminal or command prompt, navigate to the directory containing `app.py`, and run the following command to start the Flask application:
   ```
   python app.py
   ```
   This command will start the Flask development server, and you should see output indicating that the server is running.

2. Accessing the Application: Once the Flask application is running, open a web browser and navigate to `http://127.0.0.1:5000/`. You should see the homepage of the application.

3. Uploading a PDF File: On the homepage, you'll find a form where you can upload a PDF file. Click on the "Choose File" button, select a PDF file from your computer, and enter a name for the output folder in the provided text field. Then click on the "Upload and Process" button.

4. Processing the PDF File: After uploading the PDF file, the application will split each page of the PDF file into upper and lower halves. The processed files will be saved in an output folder.

5. Downloading Processed Files: Once the processing is complete, you'll be redirected to a page where you can download the processed files. You'll see a list of processed files with download links. Click on a file name to download the corresponding processed PDF file.

6. Exploring Other Pages: The application also has links to other pages (e.g., "Amazon", "Flipkart", etc.). You can click on these links to navigate to the respective pages and explore their content.

7. Stopping the Application: To stop the Flask application, you can press `Ctrl + C` in the terminal or command prompt where it is running. This will shut down the development server.



## Contact

For questions or support, contact [Uma Mina](mail to: umamina11@gmail.com).
