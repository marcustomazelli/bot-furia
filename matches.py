from playwright.sync_api import sync_playwright
from datetime import datetime
from services.insert import insert_partidas

from services.database import create_tables
create_tables()

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    page = browser.new_page()
    
    page.goto("https://www.hltv.org/team/8297/furia#tab-matchesBox")

    tabela_proximas = page.locator("table.match-table").first
    tabela_proximas.wait_for()

    partidas = tabela_proximas.locator("tbody >> tr.team-row")
    total = partidas.count()

    print(f"\nEncontrei {total} próximas partidas da FURIA:\n")

    lista_partidas = []

    for i in range(total):
        linha = partidas.nth(i)

        try:
            data = linha.locator("td.date-cell").inner_text()
            times = linha.locator("td.team-center-cell a.team-name")
            oponente = times.nth(1).inner_text()  # FURIA geralmente é o primeiro

            print(f"{data.strip()}: FURIA vs {oponente.strip()} ")

            lista_partidas.append({
                "oponente": oponente.strip(),
                "data": data.strip(),
            })

        except Exception as e:
            print(f"Erro ao processar partida {i+1}: {e}")
            continue

    insert_partidas(lista_partidas)
    browser.close()