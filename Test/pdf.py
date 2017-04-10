import re

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO


def pdf_parser(pdf_path):
    fp = file(pdf_path, 'rb')
    rsrc_mgr = PDFResourceManager()
    ret_str = StringIO()
    codec = 'utf-8'
    la_params = LAParams()
    device = TextConverter(rsrc_mgr, ret_str, codec=codec, laparams=la_params)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrc_mgr, device)
    # Process each page contained in the document.
    doc = ''
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        doc = ret_str.getvalue()
    return doc


def doc_clean(doc):
    doc_lst = doc.split('\n')
    doc_lst = [doc.strip() for doc in doc_lst if doc and doc.strip()]
    pattern = re.compile(r'[A-Z][a-z]+')
    print doc_lst
    for cnt, doc in enumerate(doc_lst):
        print cnt, doc
        # for doc in doc_lst:
        #     if pattern.match(doc):
        #         print doc


def main():
    pdf_path = r'G:\Projects\Usda\Data\abco.txt'
    doc = pdf_parser(pdf_path=pdf_path)
    doc_clean(doc)


if __name__ == '__main__':
    main()
