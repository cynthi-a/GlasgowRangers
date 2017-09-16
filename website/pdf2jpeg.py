#!/usr/bin/env python
# module PDF_TO_JPEG

import ghostscript
from pyPdf import PdfFileWriter, PdfFileReader


def pdf2jpeg(pdf_input_path, jpeg_output_path):
    args = ["pdf2jpeg",  # actual value doesn't matter
            "-dNOPAUSE",
            "-sDEVICE=jpeg",
            "-r144",
            "-sOutputFile=" + jpeg_output_path,
            pdf_input_path]
    ghostscript.Ghostscript(*args)

def multiple_pdf2jpeg(pdf_input_path, jpeg_output_path):
    print('converting {} to {}'.format(pdf_input_path, jpeg_output_path))
    inputpdf = PdfFileReader(open(pdf_input_path.format(''), "rb"))

    output_names = []
    for i in xrange(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        with open(pdf_input_path.format(i), "wb") as outputStream:
            output.write(outputStream)
        pdf2jpeg(pdf_input_path.format(i), jpeg_output_path.format(i))
        output_names.append(jpeg_output_path.format(i))
    return output_names

if __name__ == "__main__":
    pdf_input_path = "test/HackZurich2017{}.pdf"
    jpeg_output_path = pdf_input_path.replace('pdf','jpeg')
    multiple_pdf2jpeg(pdf_input_path, jpeg_output_path) 
