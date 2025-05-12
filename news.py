from playwright.sync_api import sync_playwright
from datetime import datetime
from services.insert import insert_noticias

from services.database import create_tables
create_tables()

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    page = browser.new_page()
    
    page.goto("https://www.hltv.org/")
    
    div_news = page.locator("div.standard-box.standard-list").first
    div_news.wait_for()

    news = div_news.locator("a.newsline.article")
    total = news.count()

    print(f"\nEncontrei {total} notícias do dia:\n")

    lista_noticias = []

    for i in range(total):
        linha = news.nth(i)

        # Ignora anúncios e featured
        if linha.locator("div.newstext").count() == 0:
            print(f"Notícia {i+1} ignorada: sem div.newstext (provavelmente uma featured)")
            continue

        try:
            title = linha.locator("div.newstext").inner_text()
            url = linha.get_attribute("href")

            print(f"{title.strip()}: Veja mais: https://www.hltv.org{url.strip()}")

            lista_noticias.append({
                "titulo": title.strip(),
                "link": f"https://www.hltv.org{url.strip()}",
            })
        except Exception as e:
            print(f"Erro na notícia {i+1}: {e}")
            continue

    # Salva no banco
    insert_noticias(lista_noticias)

    browser.close()