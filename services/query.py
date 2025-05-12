# services/query.py
from services.database import connect


def buscar_ultimas_partidas():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT oponente, data
        FROM partida
        ORDER BY data ASC
        LIMIT 5
    """)

    partidas = [
        {
            "oponente": row[0],
            "data": row[1]
        } for row in cursor.fetchall()
    ]

    conn.close()
    return partidas


def buscar_ultimas_noticias():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT titulo, link
        FROM noticia
        ORDER BY id DESC
        LIMIT 5
    """)

    noticias = [
        {
            "titulo": row[0],
            "link": row[1]
        } for row in cursor.fetchall()
    ]

    conn.close()
    return noticias


def buscar_stats_jogadores():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nome, rating, mapas, status
        FROM jogador
    """)

    stats = [
        {
            "nome": row[0],
            "rating": row[1],
            "mapas": row[2],
            "status": row[3]
        } for row in cursor.fetchall()
    ]

    conn.close()
    return stats


# Formatadores para o bot

def formatar_partidas(partidas):
    if not partidas:
        return "Nenhuma partida futura da FURIA encontrada."

    resposta = "Próximos jogos da FURIA:\n"
    for p in partidas:
        resposta += f"- {p['data']}: vs {p['oponente']}\n"
    return resposta


def formatar_noticias(noticias):
    if not noticias:
        return "Nenhuma notícia recente encontrada."

    resposta = "Últimas notícias da FURIA:\n"
    for n in noticias:
        resposta += f"- {n['titulo']}\n  Link: {n['link']}\n"
    return resposta


def formatar_stats(stats):
    if not stats:
        return "Nenhuma estatística de jogador encontrada."

    resposta = "Estatísticas dos jogadores da FURIA:\n"
    for s in stats:
        resposta += (
            f"- {s['nome']}\n  Rating: {s['rating']} | Mapas: {s['mapas']} | Status: {s['status']}\n"
        )
    return resposta