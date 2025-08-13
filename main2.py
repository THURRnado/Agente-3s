from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from funcoes_auxiliares import json_to_df, extrai_texto_ocr
from dotenv import load_dotenv
import json
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

def criar_agente(dados):
    instrucoes = """Você é um especialista em processamento de notas fiscais. Sua tarefa é:
    1. Analisar o texto extraído da nota fiscal
    2. Extrair APENAS os campos solicitados
    3. Retornar um JSON válido sem comentários ou texto adicional
    4. Usar a função 'json_to_df' para tratar os dados em JSON
    5. O parâmetro 'nome_arquivo' passado no 'json_to_df' deve ser composto por ('emitente_nome'+'-'+'tomador_nome') se possível
    
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
        tools=[json_to_df],
        instructions=instrucoes,
        debug_mode=True
    )

def processar(arquivo):
    try:
        print(f"Processando arquivo: {arquivo}")
        
        # Extração de texto
        dados = extrai_texto_ocr(arquivo)
        if not dados or len(dados.strip()) < 10:
            raise ValueError("Texto extraído inválido")
        
        # Criação do agente
        agent = criar_agente(dados)
        
        # Execução com tratamento de erros
        resultado = processar_com_retry(agent)
        
        if resultado:
            print("Processamento concluído com sucesso!")
            return resultado
        else:
            print("Falha ao processar o arquivo")
            return None
            
    except Exception as e:
        print(f"Erro fatal ao processar {arquivo}: {str(e)}")
        return None

if __name__ == "__main__":
    arquivo = "notas_fiscais_pdf/2025-07-28 ALBA FERNANDO NF 1000037 T 53006.pdf"
    processar(arquivo)