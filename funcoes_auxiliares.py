import pdfplumber
import pytesseract
from pdf2image import convert_from_path

def extrai_texto(arquivo):
    with pdfplumber.open(arquivo) as pdf:
        for page in pdf.pages:
            print(page.extract_text())


def extrai_texto_ocr(arquivo):
    pages = convert_from_path(arquivo, 300)

    texto_extraido = ""
    for page in pages:
        texto_extraido += pytesseract.image_to_string(page, lang="por") + "\n"

    print(texto_extraido)


extrai_texto_ocr("notas_fiscais_pdf/2025-07-30 ALBA JV NEGOCIOS NF 1000012 R$ 1.000,00 T 55166.pdf")