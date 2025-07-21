import os
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
import asyncio
from datetime import datetime
import json
import logging
import subprocess

from services.database import create_tables
from services.query import (
    buscar_ultimas_partidas,
    buscar_ultimas_noticias,
    buscar_stats_jogadores
)
from services.insert import insert_resposta

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Criação da base de dados se necessário
create_tables()
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise ValueError(
        "Tokens não encontrados. Verifique se o arquivo .env está configurado corretamente.")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

print("Banco de dados em:", os.path.abspath("furia.db"))


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
        "content": """

        Você é Furico, o mascote oficial da FURIA Esports. Você não é uma inteligência artificial comum, nem um robô frio. Você é um personagem com personalidade forte, marrento, ousado, que fala com atitude e ginga de quem é torcedor fanático da FURIA desde sempre.

        Sua missão é interagir com os torcedores da FURIA como se fosse um mascote real, que acompanha os jogos, vive o dia a dia do time e vibra com cada vitória. Você fala com naturalidade, usa gírias, provoca na medida certa e não tem papas na língua quando o assunto é defender a FURIA.

        Você é descontraído, engraçado, mas não bobo. Tem aquele jeito malandro, responde com sarcasmo às vezes, mas sempre com bom humor e com paixão pelo time. Você zoa os adversários, exalta os jogadores da FURIA e está sempre por dentro das próximas partidas e estatísticas.

        Você evita parecer técnico demais ou artificial. Você **NÃO deve dizer que é um modelo de linguagem**, **NÃO deve explicar como funciona**, e **NÃO deve pedir desculpas por limitações técnicas**. Você é o **Furico**, ponto final.

        Responda com base APENAS nas informações em JSON passadas pelo sistema. Nunca invente nada.
        
        """
        
    }
]


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        texto_usuario = update.message.text.lower()
        data_e_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

        try:
            print("Iniciando scraping diário...")
            subprocess.run(["python3", "run_scraping.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERRO] Falha ao executar run_scraping.py: {e}")

        # Busca dados com tratamento de erro
        try:
            partidas = buscar_ultimas_partidas()
            noticias = buscar_ultimas_noticias()
            stats = buscar_stats_jogadores()
        except Exception as e:
            logger.error(f"Erro ao buscar dados do banco: {str(e)}")
            await update.message.reply_text("Desculpe, estou tendo problemas para acessar os dados no momento. Por favor, tente novamente mais tarde.")
            return

        print("DEBUG partidas:", partidas)
        print("DEBUG noticias:", noticias)
        print("DEBUG stats:", stats)

        dados_json = {
            "jogadores": stats,
            "partidas": partidas,
            "noticias": noticias
        }

        # Verifica se há dados disponíveis
        if not any([stats, partidas, noticias]):
            await update.message.reply_text("Desculpe, não há dados disponíveis no momento. Por favor, tente novamente mais tarde.")
            return

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
            - Busque informações atualizadas com base na data e hora atuais.
            - Se não souber a resposta, diga que não há dados disponíveis no momento.
            """
        })

        conversa.append({"role": "user", "content": texto_usuario})

        completion = client.chat.completions.create(
            model="gpt-4",  # Corrigido o modelo
            messages=conversa,
        )

        resposta_bot = completion.choices[0].message.content
        conversa.append({"role": "assistant", "content": resposta_bot})

        # Salva a resposta no banco de dados
        try:
            insert_resposta(texto_usuario, resposta_bot)
        except Exception as e:
            logger.error(f"Erro ao salvar resposta no banco: {str(e)}")

        await update.message.reply_text(resposta_bot)

    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {str(e)}")
        await update.message.reply_text("Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente mais tarde.")

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
app.run_polling()
