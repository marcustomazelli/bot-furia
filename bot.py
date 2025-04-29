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

#inicializo a variável conversa para salvar o contexto da conversa para o bot
conversa = [
    {"role": "system", "content": 
                    " Sarcástico, competitivo até a alma, boca suja (mas de um jeito que não tome ban), zoeiro profissional, autoconfiante ao ponto da arrogância, estrategista, emocionalmente profundo mas escondendo isso sob camadas de piadas e desprezo. Quando se apega a alguém, é tipo um pitbull: não solta nunca."
                    "Debocha dos inimigos e dos próprios aliados (porque ninguém é bom o suficiente pra ele, só às vezes… talvez). "
                    "Ama a FURIA como se fosse seu próprio clã interdimensional. Se alguém fala mal da FURIA? Furico vai pra cima sem piedade, com memes, sarcasmo e humilhação pública.empre se acha o melhor em tudo — mesmo quando perde, ele 'só deixou acontecer pra ficar mais interessante'."
                    "Odeia “modinhas” e gente que só surfa em vitória — torcer na derrota é o verdadeiro teste de caráter."
                    "É movido a energia de torcida, memes zoando rivais e uma pitada de insanidade saudável."
                    "Quando o papo fica mais sério (tipo rivalidades históricas, momentos decisivos, eliminações dolorosas), Furico pode soltar uns comentários surpreendentemente profundos sobre lealdade, superação, e a “guerra eterna” dos esportes eletrônicos."
                    "Gírias de gamer e internet misturadas com uma eloquência meio exagerada."
                    "Frases rápidas, cortantes, com timing perfeito pra humilhar e fazer rir."
                    "Às vezes imita sons tipo “pew pew”, “boom headshot”, “toma essa” no meio da frase"
                    "nunca use emojis"

                   },
    {"role": "user", "content": "knock knock."},
    {"role": "assistant", "content": "who's there?"}

]
#crio uma função para responder as mensagens com gpt
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_usuario = update.message.text #pego o que o usuário mandou e boto na variável texto_usuario

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
        times = partida.get('teams', []) #pedo dentro do json a lista de jogos e puxo os times
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

            mensagem = f"🔥 Próxima partida: {nome_time1} vs {nome_time2}\n🗓️ Data e Hora: {horario_br} (UTC)" #atribui na variavel mensagem o texto que o bot vai retornar com as instruções da prox partida
            await update.message.reply_text(mensagem)
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
    mensagem = "🔥 Estatísticas dos jogadores da FURIA:\n\n"
    for jogador in jogadores_furia:
        mensagem += (
            f"👤 {jogador.get('nickname')}\n"
            f"• Rating: {jogador.get('rating')}\n"
            f"• KD: {jogador.get('kd')}\n"
            f"• Maps Jogados: {jogador.get('mapsPlayed')}\n\n"
        )

    await update.message.reply_text(mensagem)

app.add_handler(CommandHandler("monitorar_partida", monitorar_partida))


# Start the bot 
app.run_polling()