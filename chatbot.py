import google.generativeai as genai
import os
from dotenv import load_dotenv
from function import escolher_sessao, carregar_historico, exibir_historico, chat

# Carregar variáveis de ambiente
load_dotenv()

# Pega a chave API Key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API_KEY não encontrada. Verifique o arquivo .env.")

# Configurar a API Key
genai.configure(api_key=api_key)

# Criar um modelo Gemini
model = genai.GenerativeModel("gemini-1.5-flash")

# Iniciar o chatbot
chat(model)
