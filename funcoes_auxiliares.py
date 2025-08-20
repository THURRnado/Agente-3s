import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import pandas as pd

import time
import fitz


def pdf_tem_texto(arquivo):
    doc = fitz.open(arquivo)
    for page in doc:
        texto = page.get_text().strip()
        if texto:
            return True  # tem texto embutido
    return False  # provavelmente é imagem

# Não funciona pra pdfs escaneados
# Roda muito rápido, porém torna o processamento do chatbot mais lento
def extrai_texto(arquivo):
    with pdfplumber.open(arquivo) as pdf:
        texto=""
        for page in pdf.pages:
            texto += page.extract_text()
        if texto:
            print(texto)
        else:
            print("Não foi possível extrair nenhum texto!")


# Funciona para pdfs escaneados
# Roda muito mais lento, porém torna o processamento do chatbot mais rápido
def extrai_texto_ocr(arquivo):
    pages = convert_from_path(arquivo, 300)

    texto_extraido = ""
    for page in pages:
        texto_extraido += pytesseract.image_to_string(page, lang="por") + "\n"

    if texto_extraido:
        print("Texto extraido com sucesso")
        return texto_extraido
    else:
        print("Não foi possível extrair nenhum texto!")


from markitdown import MarkItDown

def extrai_texto_markitdown(arquivo):
    md = MarkItDown()  # usa OCR automaticamente em PDFs/imagens

    try:
        resultado = md.convert(arquivo)
        texto_extraido = resultado.text_content

        if texto_extraido.strip():
            print("Texto extraído com sucesso!")
            return texto_extraido
        else:
            print("Não foi possível extrair nenhum texto!")
            return ""
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        return ""



def json_to_df(nome_arquivo, json_data):
    """
    Converte dados JSON em um DataFrame do Pandas e salva em um arquivo Excel.

    Args:
        nome_arquivo (str): Nome do arquivo de saída (sem extensão).
        json_data (dict ou list): Dados no formato JSON a serem convertidos.

    Returns:
        None: A função salva o arquivo Excel no diretório atual.
    
    Example:
        >>> dados = [{"nome": "Arthur", "idade": 25}, {"nome": "Maria", "idade": 30}]
        >>> json_to_df("nota_fiscal", dados)
        # Gera o arquivo com os dados da lista.
    """
    df = pd.json_normalize(json_data)
    df.to_excel("dados_excel/" + nome_arquivo + ".xlsx", index=False)


if __name__ == "__main__":

    arquivo = "notas_fiscais_pdf/2025-07-28 ALBA FERNANDO NF 1000037 T 53006.pdf"

    print("Sem OCR\n")
    inicio = time.time()
    extrai_texto(arquivo)
    fim = time.time()
    print(f"\nTempo de execução: {(fim-inicio)}\n")
    print("/////////////////////////////////////////////////////////////////////////////////////////////")
    print("\n\nCom OCR:\n")
    inicio = time.time()
    extrai_texto_ocr(arquivo)
    fim = time.time()
    print(f"\nTempo de execução: {(fim-inicio)}\n")