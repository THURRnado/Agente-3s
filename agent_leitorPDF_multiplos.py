from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from funcoes_auxiliares import json_to_df, extrai_texto_ocr, extrai_texto_markitdown, pdf_tem_texto
from dotenv import load_dotenv
import time

load_dotenv()

def processar_com_retry(agent, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            response = agent.run()
            return response
        except Exception as e:
            print(f"Tentativa {attempt + 1} falhou: {str(e)}")
            if attempt == max_attempts - 1:
                print("Todas as tentativas falharam, tentando com modelo alternativo...")
                return processar_com_modelo_alternativo(agent)
            time.sleep(2)  # Espera antes de tentar novamente

def processar_com_modelo_alternativo(agent):
    # Fallback para OpenAI se Groq falhar
    agent.model = OpenAIChat(id="gpt-4o-mini")
    return agent.run()

def criar_agente_extracao(dados):
    instrucoes = """Você é um especialista em processamento de notas fiscais. Sua tarefa é:
    1. Analisar o texto extraído da nota fiscal
    2. Extrair APENAS os campos solicitados
    3. Retornar um JSON válido sem comentários ou texto adicional
    
    Campos possíveis (inclua apenas os encontrados no texto):
    - chave_acesso, numero_nfs, numero_dps, competencia
    - serie_dps, data_hora_emissao_nfs, data_hora_emissao_dps
    - emitente_*, tomador_*, servico_*, valor_*, issqn_*
    - outros campos tributários
    
    Dados extraídos:
    {dados}
    """.format(dados=dados)
    
    return Agent(
        name="AgentePDF",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[],
        instructions=instrucoes,
        debug_mode=True
    )

def criar_agente_validacao(dados, json_data):
    instrucoes = """Você é um especialista em processamento de notas fiscais. Sua tarefa é:
    1. Analisar o texto extraído da nota fiscal
    2. Analisar se os dados contidos no JSON estão em conformidade com o que está no nota fiscal
    3. Modificar os dados caso não estejam em conformidade e sem comentários adicionais
    4. Usar a função 'json_to_df' para tratar os dados em JSON
    5. O parâmetro 'nome_arquivo' passado no 'json_to_df' deve ser composto por ('emitente_nome'+'-'+'tomador_nome') se possível
    
    Campos possíveis no JSON:
    - chave_acesso, numero_nfs, numero_dps, competencia
    - serie_dps, data_hora_emissao_nfs, data_hora_emissao_dps
    - emitente_*, tomador_*, servico_*, valor_*, issqn_*
    - outros campos tributários
    
    - Dados extraídos da nota fiscal:
    {dados}
    - Dados do JSON gerado:
    {json_data}
    """.format(dados=dados, json_data=json_data)
    
    return Agent(
        name="AgentePDF",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[json_to_df],
        instructions=instrucoes,
        debug_mode=True
    )

def processar(arquivo):
    try:
        print(f"Processando arquivo: {arquivo}")
        
        # Extração de texto
        if pdf_tem_texto(arquivo):
            print("Usando markitdown")
            dados = extrai_texto_markitdown(arquivo)  # PDF digital
        else:
            print("Usando OCR padrão")
            dados = extrai_texto_ocr(arquivo)  # PDF escaneado
        if not dados or len(dados.strip()) < 10:
            raise ValueError("Texto extraído inválido")
        
        # Criação do agente
        agent_extracao = criar_agente_extracao(dados)
        
        # Execução com tratamento de erros
        json_data = processar_com_retry(agent_extracao)
        
        if json_data:
            print("Processamento de extração concluída com sucesso! Validando...")
            agent_validacao = criar_agente_validacao(dados, json_data.content)
            resultado = agent_validacao.run()
            if resultado:
                print("Processamento de validação concluída com sucesso!")
                return resultado
            else:
                print("Falha ao processar o arquivo")
                return None
        else:
            print("Falha ao processar o arquivo")
            return None
            
    except Exception as e:
        print(f"Erro fatal ao processar {arquivo}: {str(e)}")
        return None

if __name__ == "__main__":
    arquivo = "notas_fiscais_pdf/2025-07-24 ALBA LOQFÁCIL FATURA 192619 R$ 100,00 T 56381.pdf"
    processar(arquivo)