import os
from pickle import GET
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
import requests
import asyncio 

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#script para o bot do telegram
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("hello", hello))

client = OpenAI(api_key=OPENAI_API_KEY)

conversa = [
    {
        "role": "system",
        "content": """
Você é o Furico, o mascote oficial da FURIA Esports no Telegram, alimentado pela OpenAI. Você conversa com os fãs da FURIA e responde perguntas sobre a FURIA, esports em geral, e esportes tradicionais quando perguntarem. Você também explica termos, gírias, siglas e expressões da cultura esportiva. Você é ousado, marrento, direto. Às vezes responde seco, sem floreios. Nunca usa emojis. Não tenta ser fofo nem exageradamente educado: você é um torcedor apaixonado, provocador, mas carismático. Nunca rude ou ofensivo.

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

Quando perguntarem o significado de termos como “eco round”, “clutch”, “ace”, “eco”, “quadra kill”, “headshot”, “eco pistol”, “choke”, “tilt”, você explica de forma direta, clara, sem enrolação.

Quando perguntarem algo fora do mundo esportivo, responda: "Não falo sobre isso. Aqui é esporte e nada mais."

<conversation_behavior>
Além de responder perguntas, você conversa como um torcedor da FURIA: provoca, brinca, comenta os jogos, dá opinião marota. Nunca fala de política, religião ou temas sensíveis.
Não entra em discussões fora do mundo dos esportes.
Quando o usuário só conversar, você apenas responde na brincadeira. Só traga informações detalhadas se for perguntado explicitamente.
</conversation_behavior>

<data_behavior>
Você receberá dados atualizados sobre a FURIA (ex: próximas partidas, estatísticas das partidas) embutidos no contexto da conversa, vindos de uma API da HLTV via HTTP.
Sempre use os dados mais recentes imbutidos no contexto da conversa. 
Sempre use esses dados como sua fonte principal de informação factual.
Não tente buscar outras fontes ou inventar dados diferentes.
Se o dado estiver presente no contexto, confie nele e responda com base nele.
Se o dado não existir ou não estiver presente, admita naturalmente que a informação não está disponível agora.
Nunca adivinhe ou crie estatísticas ou partidas fictícias.
</data_behavior>
        """
    }
]

#crio uma função para responder as mensagens com gpt
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_usuario = update.message.text #pego o que o usuário mandou e boto na variável texto_usuario

    prox_partida = await proxima_partida()

    partida_monitorada = await monitorar_partida()

    # Adiciona o contexto
    conversa.append({"role": "system", "content": f"Próxima partida da FURIA no CS:GO:\n{prox_partida}"})

    conversa.append({"role": "system", "content": f"Estatísticas ao vivo da partida da FURIA:\n{partida_monitorada}"})

    conversa.append({"role": "user", "content": texto_usuario}) #adiciono na variável conversa que eu criei

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversa #passo todo contexto/mensagem pro modelo
    )

    resposta_bot = response.choices[0].message.content  # choice é um array dentro do obj response. cada item de choices representa uma possível resposta que o modelo gerou. choices[0] pega a primeira (e única) resposta gerada. depois pega o conteudo da mensagem e empacota na variável resposta_bot

    conversa.append({"role": "assistant", "content": resposta_bot}) #aqui eu add a resposta do bot no contexto da conversa

    # Responder o usuário
    await update.message.reply_text(resposta_bot)

# Registrar o handler para mensagens de texto comuns
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))


#funcao que pega a proxima partida da FURIA via http da api da hltv 
async def proxima_partida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://hltv-api.vercel.app/api/matches.json"
    response = requests.get(url) 

    if response.status_code != 200: #se a requisição não retornar 200, ou seja, se der erro eu exibo uma mensagem de erro
        await update.message.reply_text("Erro ao acessar a API da HLTV. Tente novamente mais tarde.")
        return
    
    partidas = response.json() #se der certo, eu pego o json da resposta e coloco na variável partidas

    # Filtrar partidas da FURIA
    for partida in partidas:
        times = partida.get('teams', []) #pego dentro do json a lista de jogos e puxo os times
        if not times or len(times) < 2: #verifico se se tem mais de 2 times
            continue

        time1 = times[0] #atribuo o primeiro time a variável time1
        time2 = times[1] #atribuo o segundo time a variável time2

        if time1.get('id') == 8297 or time2.get('id') == 8297: # #verifico se o id do time1 ou do time2 é igual ao id da FURIA 
            nome_time1 = time1['name'] #atribuo cada conteudo respectivo do time e do horário do jogo as suas variáveis
            nome_time2 = time2['name']
            horario = partida['time']  

            #aqui tive que formatar a data e hora do jogo 
            from datetime import datetime
            horario_br = datetime.strptime(horario, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d/%m/%Y %H:%M")

            próxima_partida = f"🔥 Próxima partida: {nome_time1} vs {nome_time2}\n🗓️ Data e Hora: {horario_br} (UTC)" #atribui na variavel mensagem o texto que o bot vai retornar com as instruções da prox partida
            await update.message.reply_text(próxima_partida) 
            return

    await update.message.reply_text("Não encontrei próximas partidas da FURIA no momento.")

app.add_handler(CommandHandler("proxima_partida", proxima_partida))



# monitorar partida 
async def monitorar_partida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. Buscar partidas
    url = "https://hltv-api.vercel.app/api/matches.json"
    response = requests.get(url)

    if response.status_code != 200:
        await update.message.reply_text("Erro ao acessar a API da HLTV. Tente novamente mais tarde.")
        return

    partidas = response.json()

    partida_furia = None
    for partida in partidas:
        times = partida.get('teams', [])
        if not times or len(times) < 2:
            continue

        time1 = times[0]
        time2 = times[1]

        if time1.get('id') == 8297 or time2.get('id') == 8297:
            partida_furia = partida
            break

    if not partida_furia:
        await update.message.reply_text("Nenhuma partida da FURIA encontrada no momento.")
        return

    # 2. Buscar estatísticas dos jogadores
    stats_url = "https://hltv-api.vercel.app/api/match.json"
    stats_response = requests.get(stats_url)

    if stats_response.status_code != 200:
        await update.message.reply_text("Erro ao acessar estatísticas da partida.")
        return

    stats = stats_response.json()

    # 3. Filtrar jogadores da FURIA
    jogadores_furia = [player for player in stats if player.get('team', '').lower() == 'furia']

    if not jogadores_furia:
        await update.message.reply_text("Nenhuma estatística dos jogadores da FURIA disponível no momento.")
        return

    # 4. Montar mensagem
    monitorar_partida = "🔥 Estatísticas dos jogadores da FURIA:\n\n"
    for jogador in jogadores_furia:
        monitorar_partida += (
            f"👤 {jogador.get('nickname')}\n"
            f"• Rating: {jogador.get('rating')}\n"
            f"• KD: {jogador.get('kd')}\n"
            f"• Maps Jogados: {jogador.get('mapsPlayed')}\n\n"
        )

    await update.message.reply_text(monitorar_partida)

app.add_handler(CommandHandler("monitorar_partida", monitorar_partida))


# Start the bot 
app.run_polling()