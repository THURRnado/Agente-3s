from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat

from funcoes_auxiliares import json_to_df, extrai_texto_ocr
from dotenv import load_dotenv

load_dotenv()


def processar(arquivo):

    dados = extrai_texto_ocr(arquivo)

    agent = Agent(
        name="Agente de pdf",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[json_to_df],
        instructions=(
            f"Aqui estão os dados extraídos da nota fiscal:\n\n"
            f"{dados}\n\n"
            "Por favor, extraia e converta esses dados em um JSON válido contendo as seguintes chaves (se presentes):\n"
            "- chave_acesso\n"
            "- numero_nfs\n"
            "- numero_dps\n"
            "- competencia\n"
            "- serie_dps\n"
            "- data_hora_emissao_nfs\n"
            "- data_hora_emissao_dps\n"
            "- emitente_nome\n"
            "- emitente_cnpj\n"
            "- emitente_endereco\n"
            "- emitente_email\n"
            "- emitente_telefone\n"
            "- tomador_nome\n"
            "- tomador_cnpj\n"
            "- tomador_endereco\n"
            "- tomador_email\n"
            "- tomador_telefone\n"
            "- servico_codigo_tributacao_nacional\n"
            "- servico_descricao\n"
            "- servico_codigo_tributacao_municipal\n"
            "- servico_local_prestacao\n"
            "- valor_servico\n"
            "- issqn_tributacao\n"
            "- issqn_retencao\n"
            "- issqn_valor\n"
            "- valor_liquido\n"
            "- irrf_retido\n"
            "- outros_tributos\n\n"
            "Retorne somente o JSON válido, sem explicações ou texto adicional.\n"
            "Depois use a função 'json_to_df' para tratar esses dados." \
            "Use o ('tomador_nome'+ '-' + 'emitente_nome') como o parametro para ser colocado no 'nome_arquivo' do 'json_to_df'"
        ),
        debug_mode=True,
    )

    agent.run()


if __name__ == "__main__":
    arquivo = "notas_fiscais_test/2025-07-28 ALBA JURACY FRANCISCO NF 62 R$ 6.500,00 T 56494.pdf"
    processar(arquivo)