import os
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
import asyncio
from datetime import datetime
import json

from services.database import create_tables
from services.query import (
    buscar_ultimas_partidas,
    buscar_ultimas_noticias,
    buscar_stats_jogadores
)
from services.insert import insert_resposta

# Criação da base de dados se necessário
create_tables()
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    intro = (
        "👋 E aí! Eu sou o Furico, o mascote da FURIA aqui no Telegram.\n\n"
        "📣 Pode perguntar sobre a FURIA, CS:GO, quais os próximos jogos, stats do jogadores e as últimas notícias do mundo esports.\n"
    )
    await update.message.reply_text(intro, parse_mode="Markdown")

app.add_handler(CommandHandler("start", start))

client = OpenAI(api_key=OPENAI_API_KEY)

conversa = [
    {
        "role": "system",
        "content": "Você é Furico, mascote da FURIA. Responda com base APENAS nas informações em JSON passadas pelo sistema. Nunca invente nada."
    }
]

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_usuario = update.message.text.lower()
    data_e_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

    partidas = buscar_ultimas_partidas()
    noticias = buscar_ultimas_noticias()
    stats = buscar_stats_jogadores()

    dados_json = {
        "jogadores": stats,
        "partidas": partidas,
        "noticias": noticias
    }

    # Adiciona contexto JSON formatado ao sistema
    conversa.append({
        "role": "system",
        "content": f"""
Hoje é {data_e_hora} (horário de Brasília).
Abaixo estão os dados disponíveis em JSON:

```json
{json.dumps(dados_json, ensure_ascii=False, indent=2)}
```

Regras:
- Responda SOMENTE se a pergunta estiver relacionada a esses dados.
- Se não souber a resposta, diga que não há dados disponíveis no momento.
"""
    })

    conversa.append({"role": "user", "content": texto_usuario})

    completion = client.chat.completions.create(
        model="gpt-4o-search-preview",
        messages=conversa,
    )

    resposta_bot = completion.choices[0].message.content
    conversa.append({"role": "assistant", "content": resposta_bot})

    await update.message.reply_text(resposta_bot)

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
app.run_polling()
