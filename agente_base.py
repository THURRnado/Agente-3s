from agno.agent import Agent
from agno.models.groq import Groq
#from agno.models.openai import OpenAIChat
from agno.playground import Playground, serve_playground_app
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory

from dotenv import load_dotenv

load_dotenv()

# OpenAIChat(id="gpt-4o-mini"),


memory = Memory(
    model=Groq(id="llama-3.3-70b-versatile"),
    db=SqliteMemoryDb(table_name="user_memories", db_file="tmp/agent_memory.db"),
)

db = SqliteStorage(table_name="agent_session", db_file="tmp/agent.db")

agent = Agent(
    name="Agente de teste",
    model=Groq(id="llama-3.3-70b-versatile"),
    memory=memory,
    enable_agentic_memory=True,
    enable_user_memories=True,
    tools=[
        
    ],
    storage=db,
    add_history_to_messages=True,
    num_history_runs=3,
    debug_mode=True,
)

app = Playground(agents=[
    agent
]).get_app()

if __name__ == "__main__":
    serve_playground_app("main:app", reload=True)

#agent.print_response("Use suas ferramentas para pesquisar temperatura de hoje em João Pessoa em Fahrenheit")