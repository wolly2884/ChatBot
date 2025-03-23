import re
import requests
import requests
import urllib3

# Desativa o aviso apenas para essa execução
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def checar_consulta(texto):
    """Verifica e consulta dados com base no texto de entrada"""
    
    # Extração de dados para consulta
    cep = extrair_cep(texto)
    cnpj = extrair_cnpj(texto)
 ##   cpf = extrair_cpf(texto) if not cnpj else None
 ##   cid = extrair_cid(texto) if not cpf and not cnpj else None
 ##   sintoma = extrair_sintoma(texto) if not cid and not cpf and not cnpj else None
 ##   vacina = extrair_vacina(texto) if not sintoma and not cid and not cpf and not cnpj else None
 ##   medicamento = extrair_medicamento(texto) if not vacina and not sintoma and not cid and not cpf and not cnpj else None
 ##   doenca = extrair_doenca(texto) if not medicamento and not vacina and not sintoma and not cid and not cpf and not cnpj else None

    # Executa a consulta apropriada
    if cep:
        return consultar_cep(cep)
    if cnpj:
        return consultar_cnpj(cnpj)
   ## if cpf:
   ##     return consultar_cpf(cpf)
   ## if cid:
   ##     return consultar_cid(cid)
   ## if sintoma:
   ##     return consultar_sintoma(sintoma)
   ## if vacina:
   ##     return consultar_vacina(vacina)
   ## if medicamento:
   ##     return consultar_medicamento(medicamento)
   ## if doenca:
   ##     return consultar_doenca(doenca)

    return None

# Funções de consulta para APIs externas
def consultar_cep(cep):
    """Consulta informações de um CEP na API ViaCEP"""
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()
        if "erro" not in dados:
            return (f"Bah, tchê! Achei o endereço pra ti: {dados['logradouro']}, "
                    f"Bairro: {dados['bairro']}, Cidade: {dados['localidade']}, "
                    f"Estado: {dados['uf']}. Capaz, tudo certinho por aí!\n")
    return "CEP inválido ou não encontrado, tchê!\n"

def consultar_cnpj(cnpj):
    """Consulta a situação cadastral de um CNPJ na Receita Federal"""
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
    headers = {"User-Agent": "ConsultaCNPJ"}  
    response = requests.get(url, headers=headers, verify=False)
    
    if response.status_code == 200:
        dados = response.json()
        if "status" in dados and dados["status"] == "ERROR":
            return "CNPJ inválido ou não encontrado.\n"
        situacao = dados.get("situacao", "Desconhecida")
        abertura = dados.get("abertura", "Desconhecida")
        tipo = dados.get("tipo", "Desconhecida")
        natureza_juridica = dados.get("natureza_juridica", "Desconhecida")
        atividade_principal = dados.get("atividade_principal", "Desconhecida")
        atividades_secundarias = dados.get("atividades_secundarias", "Desconhecida")
        nome = dados.get("nome", "Desconhecida")
        fantasia = dados.get("fantasia", "Desconhecida")
        logradouro = dados.get("logradouro", "Desconhecida")
        numero = dados.get("numero", "Desconhecida")
        municipio = dados.get("municipio", "Desconhecida")
        bairro = dados.get("bairro", "Desconhecida")
        uf = dados.get("uf", "Desconhecida")
        cep = dados.get("cep", "Desconhecida")
        email = dados.get("email", "Desconhecida")
        telefone = dados.get("telefone", "Desconhecida")
        data_situacao = dados.get("data_situacao", "Desconhecida")
        ultima_atualizacao = dados.get("ultima_atualizacao", "Desconhecida")
        capital_social = dados.get("capital_social", "Desconhecida")
        return f"O CNPJ {cnpj} está com situação cadastral: {situacao}. Nome da empresa: {nome}. Abertura: {abertura}. Tipo: {tipo}. Natureza Jurídica: {natureza_juridica}. Atividade Principal: {atividade_principal}. Atividades Secundárias: {atividades_secundarias}. Fantasia: {fantasia}. Logradouro: {logradouro}. Número: {numero}. Município: {municipio}. Bairro: {bairro}. UF: {uf}. CEP: {cep}. E-mail: {email}. Telefone: {telefone}. Data da Situação: {data_situacao}. Última Atualização: {ultima_atualizacao}. Capital Social: {capital_social}.\n"
    return "Erro ao consultar o CNPJ. Tenta de novo!\n"

## 
##### def consultar_cpf(cpf):
###    """Consulta a situação cadastral de um CPF"""
###    url = f"https://api.cpfcnpj.com.br/5d4f4e9d1d5b4c1c8e7f3c3d7b3b5d4e/1.0/cpf/{cpf}"
###    response = requests.get(url)
###    
###    if response.status_code == 200:
###        dados = response.json()
###        situacao = dados.get("situacao", "Desconhecida")
###        return f"O CPF {cpf} está com situação cadastral: {situacao}.\n"
###    return "Erro ao consultar o CPF. Tenta de novo!\n"
###
###def consultar_cid(cid):
###    """Consulta informações sobre um CID"""
###    url = f"https://disease-info-api.herokuapp.com/cids/{cid}"
###    response = requests.get(url)
###    
###    if response.status_code == 200:
###        dados = response.json()
###        return f"O CID {dados['name']} refere-se a: {dados['description']}.\n"
###    return "CID não encontrado, tchê. Tenta de novo!\n"
###
###def consultar_sintoma(sintoma):
###    """Consulta informações sobre um sintoma"""
###    url = f"https://disease-info-api.herokuapp.com/symptoms/{sintoma}"
###    response = requests.get(url)
###    
###    if response.status_code == 200:
###        dados = response.json()
###        return f"O sintoma {dados['name']} pode indicar: {dados['description']}.\n"
###    return "Sintoma não encontrado, tchê. Tenta de novo!\n"
###
###def consultar_vacina(vacina):
###    """Consulta informações sobre uma vacina"""
###    url = f"https://disease-info-api.herokuapp.com/vaccines/{vacina}"
###    response = requests.get(url)
###    
###    if response.status_code == 200:
###        dados = response.json()
###        return f"A vacina {dados['name']} protege contra: {dados['description']}.\n"
###    return "Vacina não encontrada, tchê. Vê se digitou certinho!\n"
###
###def consultar_medicamento(medicamento):
###    """Consulta informações sobre um medicamento"""
###    url = f"https://disease-info-api.herokuapp.com/medicines/{medicamento}"
###    response = requests.get(url)
###    
###    if response.status_code == 200:
###        dados = response.json()
###        return f"O medicamento {dados['name']} é usado para: {dados['description']}.\n"
###    return "Medicamento não encontrado, tchê. Tenta de novo!\n"
###
###def consultar_doenca(doenca):
###    """Consulta informações sobre uma doença"""
###    url = f"https://disease-info-api.herokuapp.com/diseases/{doenca}"
###    response = requests.get(url)
###    
###    if response.status_code == 200:
###        dados = response.json()
###        return f"Sobre a doença {dados['name']}: {dados['description']}.\n"
###    return "Doença não encontrada, tchê. Tenta de novo!\n"

# Funções de extração de padrões usando expressões regulares
####def extrair_doenca(texto):
####    match = re.search(r"\b[a-zA-Z]+\b", texto)
####    return match.group() if match else None
####
####def extrair_medicamento(texto):
####    match = re.search(r"\b[a-zA-Z]+\b", texto)
####    return match.group() if match else None
####
####def extrair_vacina(texto):
####    match = re.search(r"\b[a-zA-Z]+\b", texto)
####    return match.group() if match else None
####
####def extrair_sintoma(texto):
####    match = re.search(r"\b[a-zA-Z]+\b", texto)
####    return match.group() if match else None
####
####def extrair_cid(texto):
####    match = re.search(r"\b[A-Z]{3}\d{2}\b", texto)
####    return match.group() if match else None
####
####def extrair_cpf(texto):
####    match = re.search(r"\b\d{11}\b", texto)
####    return match.group() if match else None

def extrair_cep(texto):
    match = re.search(r"\b\d{5}-?\d{3}\b", texto)
    return match.group().replace("-", "") if match else None

def extrair_cnpj(texto):
    # Remove pontos, barras e traços
    texto_limpo = re.sub(r"[.\-/]", "", texto)

    # Procura 14 dígitos consecutivos
    match = re.search(r"\b\d{14}\b", texto_limpo)
    return match.group() if match else None
