import sqlite3


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coach (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            perfil TEXT,
            imagem TEXT,
            mapas TEXT,
            trofeus TEXT,
            winrate TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jogador (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            perfil TEXT,
            imagem TEXT,
            status TEXT,
            tempo TEXT,
            mapas TEXT,
            rating TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS noticia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            link TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS partida (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            oponente TEXT,
            data TEXT,
            evento TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS respostas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pergunta TEXT,
            resposta TEXT,
            data DATETIME
        )
    """)

    conn.commit()
    conn.close()


def connect():
    return sqlite3.connect("furia.db")
