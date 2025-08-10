from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.playground import Playground, serve_playground_app
from agno.storage.sqlite import SqliteStorage

from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
from agno.vectordb.chroma import ChromaDb

from dotenv import load_dotenv

load_dotenv()

#RAG
vector_db = ChromaDb(collection="recipes", path="tmp/chromadb")

knowledge = PDFKnowledgeBase(
    path="notas_fiscais_pdf/2025-07-31 ALBA SERGIO FLAVIO NF 54 R$ 1.320,00 T 56462.pdf",
    vector_db=vector_db,
    reader=PDFReader(chunk=True)
)
knowledge.load(recreate=True)

db = SqliteStorage(table_name="agent_session", db_file="tmp/agent.db")

agent = Agent(
    name="Agente de pdf",
    model=OpenAIChat(id="gpt-4o-mini"),
    storage=db,
    knowledge=knowledge,
    add_history_to_messages=True,
    num_history_runs=3,
    instructions="Qualquer pergunta direcionada a você está sendo feita referente aos pdfs contidos no knowledge. Ao ser pedido o que está contido nos pdfs da base de dados, apenas dê os dados contidos lá, sem colocar nenhuma informação adicional."
    # debug_mode=True,
)

app = Playground(agents=[
    agent
]).get_app()

if __name__ == "__main__":

    serve_playground_app("leitor_rag:app", reload=True)

#agent.print_response("Use suas ferramentas para pesquisar temperatura de hoje em João Pessoa em Fahrenheit")