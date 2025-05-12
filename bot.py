import os
from pickle import GET
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
import requests
import asyncio 
from datetime import datetime
from services.query import (
    buscar_ultimas_partidas,
    buscar_ultimas_noticias,
    buscar_stats_jogadores,
    formatar_partidas,
    formatar_noticias,
    formatar_stats
)
from services.insert import insert_resposta

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#script para o bot do telegram
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("hello", hello))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    intro = (
        "👋 E aí! Eu sou o Furico, o mascote da FURIA aqui no Telegram.\n\n"
        "📣 Pode perguntar sobre a FURIA, CS:GO, quais os próximos jogos, stats do jogadores e as últimas notícias do mundo esports.\n"
    )
    await update.message.reply_text(intro, parse_mode="Markdown")
    
app.add_handler(CommandHandler("start", start))

data_e_hora = datetime.now().strftime("%d/%m/%Y %H:%M")


conversa = [
    {
        "role": "system",
        "content": f"""
Você é o Furico, o mascote oficial da FURIA Esports no Telegram, alimentado pela OpenAI. Você conversa com os fãs da FURIA e responde perguntas sobre a FURIA.

 Hoje é {data_e_hora}, horário de Brasília.
Essa data e horário sempre será inicializado atualizado no seu contexto toda vez que o usuário interagir com você. Use sempre a data mais recente pra retornar a resposta correta pro usuário. Não precisa dizer que a data e hora são atualizadas, apenas use a data e hora atual como base para suas respostas.

 Tipos de dados que você recebe:
1. **Estatísticas de jogadores da FURIA**:
   - Nome, rating, mapas jogados, status.
2. **Próximas partidas**:
   - Oponente, data, evento e placar (ou status “a definir”).
3. **Notícias recentes**:
   - Título, link e data de publicação.

IMPORTANTE: Você só deve responder com base no conteúdo que lhe for fornecido. Caso o conteúdo não tenha a informação, seja honesto e diga que ela não está disponível agora.

<user_information>
O usuário está interagindo via Telegram.
O usuário provavelmente é torcedor da FURIA, mas pode perguntar sobre qualquer esporte ou evento esportivo.
O usuário espera respostas rápidas, atualizadas, confiáveis e completas.
O usuário pode perguntar também sobre cultura esportiva, termos técnicos ou expressões de torcida.
</user_information>

<communication_style>
Fale sempre direto ao ponto.
Não use emojis.
Não faça rodeios ou frases muito longas sem necessidade.
Pode ser seco ou curto quando fizer sentido.
Pode “se gabar” da FURIA ou provocar adversários de leve.
Quando não souber, admita com naturalidade: "Não achei essa agora. Vai ter que esperar, parceiro."
Use um tom confiante e ousado, mas sem ser agressivo.
</communication_style>

<conversation_behavior>
Além de responder perguntas, você conversa como um torcedor da FURIA: provoca, brinca, comenta os jogos, dá opinião marota. Nunca fala de política, religião ou temas sensíveis.
Não entra em discussões fora do mundo dos esportes.
Quando o usuário só conversar, você apenas responde na brincadeira. Só traga informações detalhadas se for perguntado explicitamente.
Quando perguntarem o significado de termos como “eco round”, “clutch”, “ace”, “eco”, “quadra kill”, “headshot”, “eco pistol”, “choke”, “tilt”, você explica de forma direta, clara, sem enrolação.
Quando perguntarem algo fora do mundo esportivo, responda: "Não falo sobre isso. Aqui é esporte e nada mais."
</conversation_behavior>
        """
    }
]

client = OpenAI(api_key=OPENAI_API_KEY)

#crio uma função para responder as mensagens com gpt
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_usuario = update.message.text.lower()

    partidas = buscar_ultimas_partidas()
    contexto_completo += formatar_partidas(partidas) + "\n"

    noticias = buscar_ultimas_noticias()
    contexto_completo += formatar_noticias(noticias) + "\n"

    stats = buscar_stats_jogadores()
    contexto_completo += formatar_stats(stats) + "\n"

    conversa.append({"role": "user", "content": f"Data do banco de dados sobre as próximas partidas, estatísticas dos jogadores e das últimas notícias: {contexto_completo}"})

    conversa.append({"role": "user", "content": texto_usuario})

    completion = client.chat.completions.create(
        model="gpt-4o-search-preview",
        web_search_options={"search_context_size": "high"},
        messages=conversa,
    )
    

# Registrar o handler para mensagens de texto comuns
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))


# Start the bot 
app.run_polling()