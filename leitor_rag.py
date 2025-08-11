from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.playground import Playground, serve_playground_app
from agno.storage.sqlite import SqliteStorage

from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
from agno.vectordb.chroma import ChromaDb

from funcoes_auxiliares import json_to_df

from dotenv import load_dotenv

load_dotenv()

arquivo = ["notas_fiscais_pdf/2025-07-28 ALBA JURACY FRANCISCO NF 62 R$ 6.500,00 T 56494.pdf","notas_fiscais_pdf/2025-07-29 ALBA JOSE ROMULO NF 1000659 R$ 250,00 T 53031.pdf","notas_fiscais_pdf/2025-07-30 ALBA JV NEGOCIOS NF 1000012 R$ 1.000,00 T 55166.pdf"]
#RAG
vector_db = ChromaDb(collection="recipes", path="tmp/chromadb")

knowledge = PDFKnowledgeBase(
    path="notas_fiscais_test/",
    vector_db=vector_db,
    reader=PDFReader(chunk=True)
)
knowledge.load(recreate=True)

db = SqliteStorage(table_name="agent_session", db_file="tmp/agent.db")

agent = Agent(
    name="Agente de pdf",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[
        json_to_df
    ],
    storage=db,
    knowledge=knowledge,
    add_history_to_messages=True,
    num_history_runs=3,
    instructions="Todas as perguntas feitas a você serão sobre os pdfs contidos no knowledge" \
    "Ao conseguir obter os dados contidos no knowledge, transforme todos que conseguir para" \
    "o modelo json. Depois utilize a função json_to_df para armazenar esses dados" \
    "O nome_do_arquivo em excel deve ser igual ao dele em pdf",
    debug_mode=True,
)

#app = Playground(agents=[
#    agent
#]).get_app()

agent.print_response("Quais os dados do pdf?")

#if __name__ == "__main__":
    #Tirar o reload True para o projeto django
    #serve_playground_app("leitor_rag:app", reload=True)