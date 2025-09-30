import threading
import time
import os
import pandas as pd
import requests
from vision import find_one_qr_code, find_location_code # Importamos a nova função
from backend import app

BACKEND_URL = "http://127.0.0.1:5000/armazenar_moto"

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def start_checkin_process(log_file):
    print("INFO: Iniciando o servidor de backend em segundo plano...")
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    time.sleep(2)

    # --- ETAPA 1: LER A MOTO ---
    moto_data = find_one_qr_code()

    if not moto_data:
        print("INFO: Processo de check-in encerrado.")
        return

    print("\n--- Dados da Moto Lidos ---")
    for key, value in moto_data.items():
        print(f"  - {key.capitalize()}: {value}")
    print("---------------------------\n")

    confirm = input("Os dados estão corretos? Deseja continuar e escanear a localização? (s/n): ").strip().lower()

    if confirm == 's':
        # --- ETAPA 2: LER A LOCALIZAÇÃO ---
        print("\nPróximo passo: escanear a localização.")
        location_code = find_location_code()

        if location_code:
            print(f"\nINFO: Enviando dados para armazenamento... Moto: {moto_data.get('placa')} -> Local: {location_code}")
            
            # --- ETAPA 3: ENVIAR DADOS COMBINADOS ---
            payload = {'moto_data': moto_data, 'log_file': log_file, 'localizacao': location_code}
            
            try:
                response = requests.post(BACKEND_URL, json=payload)
                if response.status_code == 200:
                    print(f"SUCCESS: {response.json().get('message')}")
                else:
                    print(f"ERROR: O backend retornou um erro: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                print("ERROR: Não foi possível conectar ao backend.")
        else:
            print("INFO: Armazenamento cancelado pois a localização não foi escaneada.")
    else:
        print("INFO: Armazenamento cancelado pelo usuário.")

# ... (o resto do arquivo 'main.py' e a função 'view_logs' permanecem os mesmos) ...
def view_logs():
    log_file = input("Qual arquivo de log você deseja visualizar? (ex: patio_A.csv): ").strip()
    if os.path.exists(log_file):
        try:
            df = pd.read_csv(log_file)
            print("\n--- Visualizando Log ---")
            if df.empty:
                print("O arquivo de log está vazio.")
            else:
                print(df.to_string())
            print("----------------------\n")
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
    else:
        print(f"Erro: O arquivo '{log_file}' não foi encontrado.")

def main_menu():
    print("\n" + "="*30)
    print("  Sistema de Armazenamento Mottu Vision")
    print("="*30)
    while True:
        print("\nEscolha uma opção:")
        print("  1. Fazer Check-in de uma Moto (com Webcam)")
        print("  2. Visualizar um Arquivo de Log")
        print("  3. Sair")
        choice = input("Opção: ").strip()
        if choice == '1':
            log_file = input("Digite um nome para o arquivo de log desta sessão (ex: patio_A.csv): ").strip()
            if not log_file.endswith('.csv'):
                log_file += '.csv'
            start_checkin_process(log_file)
        elif choice == '2':
            view_logs()
        elif choice == '3':
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main_menu()
