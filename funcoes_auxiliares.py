import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import pandas as pd

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