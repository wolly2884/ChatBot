import os
import json
import datetime

# Diretório para armazenar as sessões de conversa
diretorio = r"C:\tfs\chatbot-saude\venv\Conversas"
if not os.path.exists(diretorio):
    os.makedirs(diretorio)

# Contexto fixo do chatbot
contexto = """
Você é um assistente especializado na área de saúde suplementar e regulação de planos de saúde. Seu objetivo é fornecer informações detalhadas e corretas sobre coberturas, carências, rede credenciada, auditoria médica e normas da ANS.
Caso o usuário pergunte sobre:

Cobertura de procedimentos → Consulte as normas da ANS e informe se o procedimento está no Rol de Procedimentos obrigatórios.
Carência → Explique os prazos máximos permitidos pela ANS para cada tipo de atendimento.
Reembolso → Informe sobre regras e prazos para solicitação de reembolso de despesas médicas.
Auditoria médica → Explique os critérios utilizados para análise de procedimentos e solicitações médicas.
TUSS e tabelas médicas → Oriente sobre como identificar códigos e classificações de procedimentos médicos.
Autorização de exames e cirurgias → Informe sobre prazos para autorização e os direitos do beneficiário.

o valor do procedimento é de R$ 100,00 e o prazo de entrega é de 5 dias úteis.
o codigo e o 10101012 e a classificação é de 1.
o prazo para autorização é de 10 dias úteis e o beneficiário tem direito a solicitar a autorização.
"""

# Listar sessões disponíveis
def listar_sessoes():
    arquivos = [f for f in os.listdir(diretorio) if f.endswith("_user.json")]
    return sorted(arquivos, reverse=True) if arquivos else []

# Escolher uma sessão ou criar uma nova
def escolher_sessao():
    sessoes = listar_sessoes()
    if sessoes:
        print("\n📂 Sessões anteriores disponíveis:")
        for i, sessao in enumerate(sessoes):
            print(f"{i+1}. {sessao.replace('_user.json', '')}")
        escolha = input("\nDigite o número da sessão para carregar ou pressione Enter para iniciar uma nova: ").strip()
        if escolha.isdigit():
            escolha = int(escolha) - 1
            if 0 <= escolha < len(sessoes):
                base_nome = sessoes[escolha].replace("_user.json", "")
                return os.path.join(diretorio, base_nome)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(diretorio, f"chat_{timestamp}")

# Carregar histórico do arquivo
def carregar_historico(base_nome):
    user_arquivo = base_nome + "_user.json"
    assistant_arquivo = base_nome + "_assistant.json"
    
    user_history = []
    assistant_history = []
    
    if os.path.exists(user_arquivo):
        with open(user_arquivo, "r", encoding="utf-8") as file:
            try:
                user_history = json.load(file)
            except json.JSONDecodeError:
                pass
    
    if os.path.exists(assistant_arquivo):
        with open(assistant_arquivo, "r", encoding="utf-8") as file:
            try:
                assistant_history = json.load(file)
            except json.JSONDecodeError:
                pass
    
    return user_history, assistant_history

# Salvar histórico nos arquivos
def salvar_historico(base_nome, user_history, assistant_history):
    with open(base_nome + "_user.json", "w", encoding="utf-8") as file:
        json.dump(user_history, file, ensure_ascii=False, indent=4)
    with open(base_nome + "_assistant.json", "w", encoding="utf-8") as file:
        json.dump(assistant_history, file, ensure_ascii=False, indent=4)

# Exibir histórico antes de iniciar o chatbot
def exibir_historico(user_history, assistant_history):
    print("\n📜 Histórico de Usuário 📜")
    for msg in user_history:
        print(f"👤 Você: {msg}")
    
    print("\n🤖 Respostas do Chatbot 🤖")
    for msg in assistant_history:
        print(f"🤖 Chatbot: {msg}")
    
    print("\n🔹 Iniciando nova sessão 🔹\n")

# Função principal do chatbot
def chat(model):
    # Historico da sessão
    importar_historico = input("Deseja importar o histórico da sessão anterior? (s/n): ").strip().lower()
    
    # Carregar histórico das sessões anteriores
    if importar_historico != 's':
        user_history = []
        assistant_history = []
    else:
        base_nome = escolher_sessao()
        user_history, assistant_history = carregar_historico(base_nome)
        exibir_historico(user_history, assistant_history)

    # Iniciar chatbot com o contexto fixo
    print("Chatbot iniciado! Digite 'sair' para encerrar.")
    
    while True:
        user_input = input("Você: ").strip()
        if user_input.lower() == "sair":
            print("Chatbot encerrado!")
            salvar_historico(base_nome, user_history, assistant_history)
            break
        try:
            # Incluir o contexto fixo nas entradas do usuário
            full_input = contexto + "\nUsuário: " + user_input
            user_history.append(user_input)
            
            # Gerar a resposta com o modelo
            response = model.generate_content(full_input)
            assistant_history.append(response.text)
            
            print("Chatbot:", response.text)
            salvar_historico(base_nome, user_history, assistant_history)
        except Exception as e:
            print("Ocorreu um erro:", str(e))
