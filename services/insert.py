from services.database import connect


def insert_coach(coach_data):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO coach (nome, perfil, imagem, mapas, trofeus, winrate)
        VALUES (?, ?, ?, ?, ?, ?)
    """, coach_data)
    conn.commit()
    conn.close()


def insert_jogadores(lista_jogadores):
    conn = connect()
    cursor = conn.cursor()
    for jogador in lista_jogadores:
        cursor.execute("""
            INSERT INTO jogador (nome, perfil, imagem, status, tempo, mapas, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, jogador)
    conn.commit()
    conn.close()


def insert_noticias(lista_noticias):
    conn = connect()
    cursor = conn.cursor()
    for noticia in lista_noticias:
        cursor.execute("""
            INSERT INTO noticia (titulo, link)
            VALUES (?, ?)
        """, (
            noticia["titulo"],
            noticia["link"]
        ))
    conn.commit()
    conn.close()


def insert_partidas(lista_partidas):
    conn = connect()
    cursor = conn.cursor()
    for partida in lista_partidas:
        cursor.execute("""
            INSERT INTO partida (oponente, data, evento)
            VALUES (?, ?, ?)
        """, (
            partida["oponente"],
            partida["data"],
            partida["evento"]
        ))
    conn.commit()
    conn.close()


def insert_resposta(pergunta, resposta):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO respostas (pergunta, resposta, data) VALUES (?, ?, datetime('now'))",
        (pergunta, resposta)
    )
    conn.commit()
    conn.close()
