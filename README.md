# Chatbot de Saúde Suplementar

Este é um chatbot especializado em **saúde suplementar**, que responde perguntas sobre **planos de saúde, coberturas, carências, reembolsos, auditorias médicas, normas da ANS, endereços CEP e CNPJs de empresas**. Após três perguntas, o chatbot gera um resumo dos principais pontos abordados na conversa.

## Tecnologias Utilizadas
- **Python 3**
- **Google Generative AI (Gemini 1.5 Flash)**
- **Requests** (para consultas a APIs externas)
- **Dotenv** (para variáveis de ambiente)

## Estrutura do Projeto
```
chatbot-saude/
│── Conversas/             # Armazena o histórico de conversações
│── chatbot.py             # Script principal para iniciar o chatbot
│── function.py            # Gerencia histórico e interação com o chatbot
│── Consultas.py           # Consulta CEPs e CNPJs via APIs externas
│── .env                   # Contém a chave da API Gemini (não incluído no repositório)
│── requirements.txt       # Lista de dependências do projeto
```

## Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/chatbot-saude.git
   cd chatbot-saude
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```sh
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

4. Crie um arquivo `.env` e adicione sua chave de API Gemini:
   ```sh
   GEMINI_API_KEY=your_api_key_here
   ```

## Como Usar

Para iniciar o chatbot, execute:
```sh
python chatbot.py
```

O chatbot perguntará se deseja carregar o histórico de conversas anteriores. O usuário pode fazer **até três perguntas** antes que um resumo seja gerado.

## Funcionalidades
- **Responde perguntas sobre saúde suplementar** com foco em planos de saúde, coberturas, carências, reembolsos e auditoria médica.
- **Consulta CEPs** utilizando a API do ViaCEP.
- **Consulta CNPJs** de empresas usando a API da ReceitaWS.
- **Histórico de conversa** salvo automaticamente no diretório `Conversas/`.
- **Respostas com tom amigável** e expressões do interior do Rio Grande do Sul.

## Exemplo de Uso
```
Deseja importar o histórico da sessão anterior? (s/n): s

📜 Histórico de Usuário 📜
👤 Você: Qual a carência para internações?
🤖 Chatbot: Bah, tchê! O prazo de carência para internações e cirurgias é de 180 dias.

🔹 Iniciando nova sessão 🔹

Você: Qual o reembolso para consultas?
Chatbot: O valor do reembolso é de R$ 50,00 e o prazo para pagamento é de 30 dias.

🔹🔹🔹 RESUMO FINAL 🔹🔹🔹
- Carência para internações: 180 dias.
- Reembolso para consultas: R$ 50,00, prazo de 30 dias.
```
## Vídeo Demonstrativo

Veja o chatbot em ação neste vídeo: YouTube

## Problemas Conhecidos
- Algumas consultas de CNPJ podem falhar devido a certificados SSL. Se isso ocorrer, tente **atualizar os certificados CA** ou desativar a verificação SSL (temporariamente) em `Consultas.py`.

## Contribuição
Pull requests são bem-vindos! Para grandes alterações, abra uma issue primeiro para discutir o que deseja modificar.

## Licença
Este projeto está sob a licença MIT.

