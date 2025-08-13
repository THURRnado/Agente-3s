from agno.agent import Agent
from agno.app.whatsapp.app import WhatsappAPI
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import os

load_dotenv()

# Configuração do Agente
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions="Você é um assistente de WhatsApp profissional...",
    add_history_to_messages=True,
    markdown=True
)

# Configuração WhatsApp
whatsapp_app = WhatsappAPI(
    agent=agent,
    name="Assistente Virtual",
    app_id="assistente_virtual",
    description="Atendimento automático via WhatsApp",
    # Adicione estas configurações quando tiver as credenciais:
    # access_token=os.getenv("WHATSAPP_ACCESS_TOKEN"),
    # phone_number_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID"),
    # verify_token=os.getenv("WHATSAPP_VERIFY_TOKEN")
)

# Obtenha a aplicação FastAPI
app = whatsapp_app.get_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "whatsapp_agent:app",  # Alterado para apontar para o arquivo/modulo correto
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )