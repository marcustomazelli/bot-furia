import subprocess
import sys

scripts = ["matches.py", "news.py", "stats.py"]

for script in scripts:
    print(f"Executando {script}...")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"[ERRO] Falha ao executar {script}")
    else:
        print(f"{script} executado com sucesso!\n")

print("Scraping diário finalizado.")
