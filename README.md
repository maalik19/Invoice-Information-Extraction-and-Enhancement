# Invoice-Information-Extraction-and-Enhancement

The "Invoice-Information-Extraction-and-Enhancement" project is designed to automatically extract important information from invoices and enhance the extracted data for further processing. It utilizes Flask, a web framework for building web applications, and EasyOCR, a Python library for optical character recognition. In this overview, we will discuss the main functionalities and goals of this project without going into the code details.

The project involves the following main steps:

1.Image Upload and Display:

The Flask web application accepts image file uploads through a specified route.
The uploaded image is displayed in a web page using Matplotlib, allowing users to visualize the original image.

2.Text Detection and Recognition:

EasyOCR is used to perform text detection and recognition on the uploaded invoice image.
Multiple languages, such as English and French, are supported for text recognition.
Text regions are identified, and the corresponding text and detection scores are extracted.

3.Information Extraction:

The project extracts various pieces of information from the detected text on the invoice.
This includes details such as the invoice date, phone numbers, client name, and total amount (Total TTC).
Special attention is given to detecting the "DESIGNATION" section on the invoice.

4.Data Enhancement:

The project enhances the detected data, especially the "DESIGNATION" section, by expanding the bounding box and combining related text entries.
The enhanced data is highlighted for clarity, making it easier to identify important invoice details.

5.JSON Data Output:

The extracted and enhanced data is structured into a JSON format, which is well-organized and easily readable.
The JSON data is saved in a file for further use or analysis.
