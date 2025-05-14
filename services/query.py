# services/query.py
from services.database import connect


def buscar_ultimas_partidas():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT oponente, data, evento
        FROM partida
        ORDER BY data ASC
        LIMIT 5
    """)

    partidas = [
        {
            "oponente": row[0],
            "data": row[1],
            "evento": row[2]
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
