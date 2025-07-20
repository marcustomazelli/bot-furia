# Furico - Bot Oficial da FURIA no Telegram

**Furico** é um chatbot com inteligência artificial criado especialmente para os torcedores da **FURIA Esports**. Desenvolvido em **Python**, o projeto integra a **API da OpenAI** com o **Telegram** para criar uma experiência de conversa natural e divertida com o mascote virtual do time.

---

## Objetivo

Oferecer aos fãs da FURIA uma maneira interativa e descontraída de se manterem atualizados com:

- Notícias recentes da FURIA
- Estatísticas dos jogadores
- Informações sobre próximas partidas
- Conversas contínuas com o mascote **Furico**, que possui uma personalidade única e marcante

---

## Personalidade do Furico

Furico não é apenas um bot. Ele é o mascote **marrento**, **provocativo** e **descontraído** da FURIA.  
O objetivo foi criar um modelo conversacional que parecesse o mais natural possível — como se o torcedor estivesse trocando ideia com alguém real, e não com uma IA.

---

## Tecnologias Utilizadas

- **Python** – Linguagem principal do projeto  
- **OpenAI API** – Geração de respostas conversacionais com IA  
- **Telegram Bot API** – Integração e comunicação com usuários no Telegram  
- **Playwright** – Web Scraping de dados do site [HLTV.org](https://www.hltv.org)  
- **SQLite** – Banco de dados local para armazenar mensagens, estatísticas e dados da FURIA

---

## Como Funciona

1. **Interação com o usuário no Telegram**  
   Usuários enviam mensagens para o bot no Telegram.

2. **Processamento da mensagem**  
   A mensagem é registrada no banco de dados e enviada para a API da OpenAI com o contexto da conversa.

3. **Geração de resposta personalizada**  
   A IA responde de forma natural, mantendo o estilo provocativo do Furico. A resposta também é salva no banco.

4. **Consulta de informações externas**  
   Furico responde com:
   - Estatísticas atualizadas dos jogadores
   - Últimas notícias da FURIA
   - Próximas partidas  

   Tudo isso é feito com scraping em tempo real usando o Playwright, com cache dos dados no SQLite.

5. **Resposta ao usuário**  
   A resposta final é formatada e enviada para o usuário no Telegram.

---

## Como Rodar Localmente

> Pré-requisitos: Python 3.10+, Playwright, SQLite3, token do Telegram Bot, chave da API OpenAI.

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/furico-bot.git
cd furico-bot

# Instalar as dependências
pip install -r requirements.txt

# Instalar os navegadores do Playwright
playwright install

# Criar e configurar o arquivo .env
TELEGRAM_BOT_TOKEN=seu_token_do_telegram
OPENAI_API_KEY=sua_chave_da_openai

# Executar o bot
python bot/main.py


