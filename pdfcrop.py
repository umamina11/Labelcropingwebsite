#!/usr/bin/env python
# coding: utf-8

# In[9]:


import os
import PyPDF2

def split_pdf(input_pdf, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        for page_num in range(len(reader.pages)):
            writer = PyPDF2.PdfWriter()
            output_pdf = f"{output_folder}/page_{page_num + 1}.pdf"
            writer.add_page(reader.pages[page_num])
            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)
            print(f"Page {page_num + 1} saved as {output_pdf}")

# Example usage:
input_pdf = 'Sample1.pdf'  # Input PDF file path
output_folder = 'output_pages'  # Output folder path

split_pdf(input_pdf, output_folder)



# In[ ]:




