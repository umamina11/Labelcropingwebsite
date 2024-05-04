#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install PyPDF2')


# In[7]:


import os
import PyPDF2

def split_and_crop_pdf(input_pdf, output_folder, label_dimensions):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            cropped_page = (page.cropbox.lower_left + page.cropbox.upper_right +
                            label_dimensions)
            page.cropbox.lower_left = (cropped_page[0], cropped_page[1])
            page.cropbox.upper_right = (cropped_page[2], cropped_page[3])
            
            writer = PyPDF2.PdfWriter()
            output_pdf = f"{output_folder}/page_{page_num + 1}.pdf"
            writer.add_page(page)
            
            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)
            print(f"Page {page_num + 1} saved as {output_pdf}")

# Convert inches to points (1 inch = 72 points)
label_dimensions_inches = (4, 6)
label_dimensions_points = tuple(dim * 72 for dim in label_dimensions_inches)

# Example usage:
input_pdf = 'Sample1.pdf'  # Input PDF file path
output_folder = 'outputfolder'  # Output folder path

split_and_crop_pdf(input_pdf, output_folder, label_dimensions_points)



# In[29]:


import os
import PyPDF2

def split_and_crop_pdf(input_pdf, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
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
            print(f"Upper half of page {page_num + 1} saved as {output_pdf}")

# Example usage:
input_pdf = 'Sample1.pdf'  # Input PDF file path
output_folder = 'upper'  # Output folder path

split_and_crop_pdf(input_pdf, output_folder)



# In[ ]:





# In[ ]:




