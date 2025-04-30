# Furico Bot

**Furico** é um bot para Telegram criado com Python. Ele representa o mascote não oficial da FURIA Esports e possui integração com a OpenAI e a API da HLTV. Seu comportamento é baseado em uma personalidade sarcástica e fanática, com respostas dinâmicas geradas por inteligência artificial. Além disso, o bot consulta partidas futuras e estatísticas de jogadores da FURIA em tempo real.

---

## Funcionalidades

- **Respostas com personalidade:** Interação natural e contínua com o usuário via modelo da OpenAI.
- **Comando `/hello`:** Cumprimenta o usuário.
- **Comando `/proxima_partida`:** Informa a próxima partida da FURIA com data e horário.
- **Comando `/monitorar_partida`:** Exibe estatísticas dos jogadores da FURIA na partida atual.
- **Contexto de conversa preservado:** Histórico de mensagens mantido para respostas com mais coerência.

---

## Tecnologias utilizadas

- [Python 3.10+](https://www.python.org/)
- [python-telegram-bot](https://docs.python-telegram-bot.org/en/stable/)
- [OpenAI API](https://platform.openai.com/)
- [requests](https://docs.python-requests.org/)
- [dotenv](https://pypi.org/project/python-dotenv/)
- [HLTV Unofficial API](https://hltv-api.vercel.app/)

## Observações Importantes

- A API da HLTV utilizada atualmente no projeto é uma versão não-oficial e encontra-se desatualizada desde 2022.
- A lógica de consumo da API via HTTP está completamente funcional e validada.
- O que falta é substituir a API antiga por uma nova fonte confiável e atualizada em tempo real, com dados do cenário competitivo atual.
- No momento, **não existe nenhuma API gratuita e não-oficial disponível** que forneça esses dados em tempo real de forma consistente.
- O acesso a APIs atualizadas e em tempo real exige normalmente **contratação de serviços pagos**, o que não se justifica neste caso por se tratar de um **protótipo voltado para um desafio técnico**.
- Assim que uma nova API (oficial ou extraoficial) estiver disponível, basta substituir a URL e adaptar pequenos pontos do JSON, mantendo toda a estrutura lógica do código intacta.