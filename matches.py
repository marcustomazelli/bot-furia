from playwright.sync_api import sync_playwright
from services.insert import insert_partidas
from services.database import create_tables

create_tables()

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    page = browser.new_page()

    page.goto("https://www.hltv.org/team/8297/furia#tab-matchesBox")
    page.wait_for_selector("table.match-table")

    # Pega todos os blocos de evento e os seus tbody correspondentes
    tabela = page.locator("table.match-table").first
    eventos = tabela.locator("tr.event-header-cell")
    blocos_partidas = tabela.locator("tbody")

    total = eventos.count()

    for i in range(total):
        evento = eventos.nth(i)

        # Pega o nome do evento
        if evento.locator("a").count() == 0:
            continue

        event_name = evento.locator("a").inner_text().strip()

        # Verifica se ainda estamos em 'Upcoming matches'
        # Se o evento for posterior ao texto "Recent results for FURIA", paramos o loop
        if "recent results" in event_name.lower():
            break

        partidas = blocos_partidas.nth(i).locator("tr.team-row")

        for j in range(partidas.count()):
            linha = partidas.nth(j)
            try:
                data = linha.locator("td.date-cell").inner_text().strip()
                times = linha.locator("td.team-center-cell a.team-name")
                if times.count() < 2:
                    continue

                oponente = times.nth(1).inner_text().strip()

                print(f"{data}: FURIA vs {oponente} – {event_name}")

                insert_partidas([{
                    "oponente": oponente,
                    "data": data,
                    "evento": event_name,
                }])

                print("Inserido no banco:", {
                    "oponente": oponente,
                    "data": data,
                    "evento": event_name,
                })
            except Exception as e:
                print(f"[Erro na partida] {e}")

    browser.close()
