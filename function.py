import os
import json
import datetime
from Consultas import checar_consulta

# Diretório para armazenar conversas
diretorio = r"C:\tfs\chatbot-saude\Conversas"
if not os.path.exists(diretorio):
    os.makedirs(diretorio)

# Número máximo de perguntas antes do resumo
MAX_PERGUNTAS = 3

##########################################################################################################################
##    Lista as sessões de conversa disponíveis.                                                                         ##    
##    Esta função lista todos os arquivos no diretório especificado que terminam com "_user.json".                      ##
##    Os arquivos são retornados em uma lista ordenada em ordem decrescente. Se não houver arquivos,                    ##     
##    uma lista vazia é retornada.                                                                                      ##                                               
##    Returns:                                                                                                          ##
##        list: Uma lista de nomes de arquivos que representam as sessões de conversa, ordenada em ordem decrescente.   ##
##########################################################################################################################
def listar_sessoes():
 
    """Lista as sessões de conversa disponíveis."""
    arquivos = [f for f in os.listdir(diretorio) if f.endswith("_user.json")]
    return sorted(arquivos, reverse=True) if arquivos else []

##########################################################################################################################
##    Exibe o histórico de conversa.                                                                                    ##
##    Args:                                                                                                             ##
##        user_history (list): O histórico do usuário.                                                                  ##
##        assistant_history (list): O histórico do assistente.                                                          ##
##########################################################################################################################
def exibir_historico(user_history, assistant_history):
    print("\n📜 Histórico de Usuário 📜")
    for msg in user_history:
        print(f"👤 Você: {msg}")
    
    print("\n🤖 Respostas do Chatbot 🤖")
    for msg in assistant_history:
        print(f"🤖 Chatbot: {msg}")
    
    print("\n🔹 Iniciando nova sessão 🔹\n")
##########################################################################################################################
##    Escolhe uma sessão existente ou cria uma nova.                                                                    ##
##    Args:                                                                                                             ##
##        importar_historico (str): Indica se deve importar o histórico ('s' para sim, qualquer outra coisa para não).  ##
##    Returns:                                                                                                          ##
##        tuple: Um par de strings contendo o nome da base escolhida e o nome da nova base.                             ##
##########################################################################################################################
def escolher_sessao(importar_historico):
 
    """Escolhe uma sessão existente ou cria uma nova."""
    data_atual = datetime.datetime.now().strftime("%Y%m%d")
    sessoes = listar_sessoes()

    base_escolhida = f"chat_{data_atual}"
    base_nova = f"chat_{data_atual}"
    if importar_historico == 's': 
        if sessoes:
            print("\n📂 Sessões anteriores disponíveis:")
            for i, sessao in enumerate(sessoes):
                print(f"{i+1}. {sessao.replace('_user.json', '')}")

            escolha = input("\nDigite o número da sessão para carregar ou pressione Enter para iniciar uma nova: ").strip()

            if escolha.isdigit():
                escolha = int(escolha) - 1
                if 0 <= escolha < len(sessoes):
                    base_escolhida = sessoes[escolha].replace("_user.json", "")
                    if data_atual in base_escolhida:
                        return base_escolhida, base_nova 

    return base_escolhida, base_nova

##########################################################################################################################
##    Carrega o histórico de uma sessão de conversa.                                                                    ##
##    Args:                                                                                                             ##
##        base_nome (str): O nome da base de dados da sessão.                                                           ##
##    Returns:                                                                                                          ##
##        tuple: Um par de listas contendo o histórico do usuário e do assistente.                                      ##
##########################################################################################################################
def carregar_historico(base_nome):

    """Carrega o histórico de uma sessão de conversa."""
    user_arquivo = os.path.join(diretorio, base_nome + "_user.json")
    assistant_arquivo = os.path.join(diretorio, base_nome + "_assistant.json")
    
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

##########################################################################################################################
##    Salva o histórico da sessão.                                                                                      ##
##    Args:                                                                                                             ##
##        base_nome (str): O nome da base de dados da sessão.                                                           ##
##        user_history (list): O histórico do usuário.                                                                  ##
##        assistant_history (list): O histórico do assistente.                                                          ##
##########################################################################################################################
def salvar_historico(base_nome, user_history, assistant_history):
    """Salva o histórico da sessão."""
    base_nome = os.path.join(diretorio, base_nome)

    with open(base_nome + "_user.json", "w", encoding="utf-8") as file:
        json.dump(user_history, file, ensure_ascii=False, indent=4)
    with open(base_nome + "_assistant.json", "w", encoding="utf-8") as file:
        json.dump(assistant_history, file, ensure_ascii=False, indent=4)

##########################################################################################################################
##    Inicia a conversa com o chatbot, permitindo três perguntas e gerando um resumo final.                             ##
##    Args:                                                                                                             ##
##        model (Chatbot): O modelo do chatbot.                                                                         ##
##########################################################################################################################
def chat(model):
    """Inicia a conversa com o chatbot."""
    importar_historico = input("Deseja importar o histórico da sessão anterior? (s/n): ").strip().lower()
    base_escolhida, base_nova = escolher_sessao(importar_historico)
    
    if importar_historico == 's':
        user_history, assistant_history = carregar_historico(base_escolhida)
        exibir_historico(user_history, assistant_history)
    else:
        user_history, assistant_history = [], []
    
    print("Chatbot iniciado! Você pode fazer até três perguntas. Digite 'sair' para encerrar.")
    contador_perguntas = 0
    
    while contador_perguntas < MAX_PERGUNTAS:
        user_input = input("Você: ").strip()
        if user_input.lower() == "sair":
            break
        
        user_history.append(user_input)
        resposta = checar_consulta(user_input)  

        if not resposta:
            prompt_ajustado = (
                "Responda de forma amigável, como se fosse um gaúcho do interior conversando com um amigo. "
                "Use expressões como 'bah', 'tchê', 'guria', 'guri', 'capaz', 'mas bah', 'tri', 'bagual', "
                "'barbaridade', 'coisa séria' e 'é de cair os butia do bolso'. Mantenha a resposta clara e objetiva sobre saúde suplementar. "
                "Aqui está a pergunta do usuário:\n"
                f"{user_input}"
            )
        else:
            prompt_ajustado = (
                "Responda de forma amigável, como se fosse um gaúcho do interior conversando com um amigo. "
                "Use expressões como 'bah', 'tchê', 'guria', 'guri', 'capaz', 'mas bah', 'tri', 'bagual', "
                "'barbaridade', 'coisa séria' e 'é de cair os butia do bolso'. "
                "Aqui está a pergunta do usuário:\n"
                f"{resposta}"
            )

        resposta = model.generate_content(prompt_ajustado).text
        assistant_history.append(resposta)
        
        print("Chatbot:", resposta)
        contador_perguntas += 1
        salvar_historico(base_nova, user_history, assistant_history)
        
        if contador_perguntas == 3:
            print("\n🔹🔹🔹 RESUMO PARCIAL 🔹🔹🔹\n")
            respostas_chatbot = "\n".join(assistant_history[-3:])
            resumo_parcial = model.generate_content(f"Resuma as seguintes respostas do chatbot:\n{respostas_chatbot}").text
            assistant_history.append("\nResumo parcial:\n" + resumo_parcial)
            print(resumo_parcial)
    
    print("\n🔹🔹🔹 RESUMO FINAL 🔹🔹🔹\n")
    respostas_chatbot = "\n".join(assistant_history)
    resumo_final = model.generate_content(f"Resuma as seguintes respostas do chatbot:\n{respostas_chatbot}").text
    assistant_history.append("\nResumo final:\n" + resumo_final)
    print(resumo_final)
    salvar_historico(base_nova, user_history, assistant_history)
    print("\nChatbot encerrado!")