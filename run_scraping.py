import schedule
import subprocess
import sys
import time
from datetime import datetime


scripts = ["matches.py", "news.py", "stats.py"]

def scraping_diario():
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando scraping diário...")
    for script in scripts:
        print(f"Executando {script}...")
        result = subprocess.run([sys.executable, script])
        if result.returncode != 0:
            print(f"[ERRO] Falha ao executar {script}")
        else:
            print(f"{script} executado com sucesso!\n")
    print("Scraping diário finalizado.\n")

# agendando para rodar todos os dias às 09:00 da manhã
schedule.every().day.at("09:00").do(scraping_diario)


print("[INFO] Agendador iniciado. Aguardando horário programado...")


while True:
    schedule.run_pending()
    time.sleep(60)  # checa a cada 1 minuto
