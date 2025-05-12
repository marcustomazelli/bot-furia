from playwright.sync_api import sync_playwright
from services.database import create_tables
from services.insert import insert_coach, insert_jogadores

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    page = browser.new_page()
    
    page.goto("https://www.hltv.org/team/8297/furia#tab-rosterBox")
    
    # Coach
    page.wait_for_selector("table.coach-table")
    coach_row = page.locator("table.coach-table tr")
    coach_cell = coach_row.locator("td.playersBox-first-cell a.playersBox-playernick-image")
    
    coach_name = coach_cell.locator("div.playersBox-playernick div.text-ellipsis").inner_text()
    coach_link = coach_cell.get_attribute("href")
    imagem_url = coach_cell.locator("div.playersBox-img-wrapper img.playerBox-bodyshot").get_attribute("src")
    maps_played = coach_row.locator("div.players-cell.center-cell.opacity-cell").nth(1).inner_text()
    trophies = coach_row.locator("div.players-cell.center-cell.opacity-cell").nth(2).inner_text()
    win_rate = coach_row.locator("div.players-cell.rating-cell").inner_text()

    print(f"Coach da FURIA: {coach_name.strip()}")
    print(f"Perfil: https://www.hltv.org{coach_link.strip()}")
    print(f"Imagem: {imagem_url.strip()}")
    print(f"Mapas jogados: {maps_played.strip()}")
    print(f"Troféus: {trophies.strip()}")
    print(f"Win Rate: {win_rate.strip()}")

    # Cria tabelas antes de tudo
    create_tables()

    # Jogadores
    page.wait_for_selector("table.players-table")
    page.wait_for_timeout(500)  # Espera o DOM se estabilizar
    player_rows = page.locator("table.players-table tr")
    total_players = player_rows.count()
    
    print(f"\nEncontrei {total_players} jogadores na FURIA:\n")

    jogadores = []
  
    for i in range(total_players):
        row = player_rows.nth(i)
        
        try:
            name_locator = row.locator("td.playersBox-first-cell a.playersBox-playernick-image div.playersBox-playernick.text-ellipsis div.text-ellipsis")
            name = name_locator.inner_text(timeout=2000)
        except:
            print(f"Linha {i+1} ignorada: não contém jogador")
            continue
        
        link = row.locator("td.playersBox-first-cell a.playersBox-playernick-image").get_attribute("href") or ""
        image = row.locator("td.playersBox-first-cell a.playersBox-playernick-image div.playersBox-img-wrapper img.playerBox-bodyshot").get_attribute("src") or ""

        # Dados
        status = "N/A"
        time_on_team = "N/A"
        maps_played = "N/A"
        rating = "N/A"

        try:
            status_locator = row.locator("div.status-cell div.player-status")
            if status_locator.count() > 0:
                status = status_locator.text_content(timeout=0).strip()
        except:
            pass

        try:
            time_locator = row.locator("div.center-cell.opacity-cell").nth(0)
            if time_locator.count() > 0:
                time_on_team = time_locator.text_content(timeout=0).strip()
        except:
            pass

        try:
            maps_locator = row.locator("div.center-cell.opacity-cell").nth(1)
            if maps_locator.count() > 0:
                maps_played = maps_locator.text_content(timeout=0).strip()
        except:
            pass

        try:
            rating_locator = row.locator("div.rating-cell")
            if rating_locator.count() > 0:
                rating = rating_locator.text_content(timeout=0).strip()
        except:
            pass

        print(f"Jogador {i+1}: {name.strip()}")
        print(f"  Perfil: https://www.hltv.org{link.strip()}")
        print(f"  Imagem: {image.strip()}")
        print(f"  Status: {status}")
        print(f"  Tempo na equipe: {time_on_team}")
        print(f"  Mapas jogados: {maps_played}")
        print(f"  Rating: {rating}\n")

        jogadores.append({
            "nome": name.strip(),
            "perfil": f"https://www.hltv.org{link.strip()}",
            "imagem": image.strip(),
            "status": status,
            "tempo": time_on_team,
            "mapas": maps_played,
            "rating": rating
        })

    insert_coach((
        coach_name,
        f"https://www.hltv.org{coach_link}",
        imagem_url,
        maps_played,
        trophies,
        win_rate
    ))

    insert_jogadores([
        (
            jogador["nome"],
            jogador["perfil"],
            jogador["imagem"],
            jogador["status"],
            jogador["tempo"],
            jogador["mapas"],
            jogador["rating"]
        )
        for jogador in jogadores
    ])

    browser.close()