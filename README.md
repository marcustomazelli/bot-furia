# Furico Bot

**Furico** é um bot para Telegram criado com Python. Ele representa o mascote não oficial da FURIA Esports e combina inteligência artificial com informações atualizadas do cenário competitivo. Sua personalidade ousada, fanática e sarcástica oferece uma experiência de interação única para os fãs da FURIA.

O bot utiliza a API da OpenAI para gerar respostas com base em uma técnica chamada **RAG (Retrieval-Augmented Generation)**, que permite ao modelo de linguagem responder com base em informações externas buscadas em tempo real via API da HLTV.

**Link no Telegram:** [@FuricoFuriosoBot](https://t.me/FuricoFuriosoBot)

---

## Funcionalidades

- **Respostas com personalidade:** Interação natural com o usuário via modelo da OpenAI, incorporando a personalidade "Furico" no estilo torcedor fanático e provocador.
- **RAG (Retrieval-Augmented Generation):** Integração da IA com dados buscados em tempo real por APIs externas, permitindo que a IA responda baseada em informações atualizadas sobre próximas partidas, estatísticas dos jogadores e notícias sobre esports.
- **Contexto dinâmico:** Cada resposta da IA é enriquecida com dados atualizados da API antes de ser gerada, garantindo respostas mais precisas e confiáveis.
- **Histórico de conversa preservado:** Mantém o contexto das conversas para interações mais naturais e coerentes.

---

## Tecnologias utilizadas

- [Python 3.10+](https://www.python.org/)
- [python-telegram-bot](https://docs.python-telegram-bot.org/en/stable/)
- [OpenAI API](https://platform.openai.com/)
- [HLTV Unofficial API](https://hltv-api.vercel.app/)

---

## Sobre a técnica RAG

O **Furico Bot** utiliza a técnica **RAG (Retrieval-Augmented Generation)**, onde o modelo de linguagem recebe informações atualizadas de fontes externas (via API) injetadas no prompt antes da geração da resposta.

Esse método permite que a IA:

- Responda com base em dados atualizados de **próximas partidas**, **estatísticas de jogadores** e **notícias do cenário**.
- Evite alucinações e informações desatualizadas que poderiam ocorrer caso dependesse apenas do modelo treinado.
- Atue como um **assistente contextualizado em tempo real**, confiando sempre nos dados da API fornecidos no contexto da conversa.

---

## Observações Importantes

- A API da HLTV utilizada atualmente no projeto é uma versão **não-oficial e encontra-se desatualizada desde 2022**.
- A lógica de consumo da API via HTTP está **funcional e validada** para as rotas existentes.
- No momento, **não existe nenhuma API gratuita e não-oficial disponível que forneça dados 100% atualizados em tempo real de forma confiável**.
- APIs oficiais ou atualizadas normalmente exigem **contratação de serviços pagos**, o que não se justifica por se tratar de um **protótipo voltado para um desafio técnico**.
- Caso uma nova API atualizada esteja disponível no futuro, será necessário apenas **atualizar as URLs e adaptar o parse do JSON**, mantendo toda a lógica do bot.