from flask import Flask, request, jsonify
import csv
import os
from datetime import datetime

app = Flask(__name__)

def init_csv(csv_file):
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['timestamp', 'placa', 'chassi', 'modelo', 'km', 'contrato', 'ocorrencia', 'localizacao'])

@app.route('/armazenar_moto', methods=['POST'])
def armazenar_moto():
    data = request.get_json()
    if not data or 'moto_data' not in data or 'log_file' not in data or 'localizacao' not in data:
        return jsonify({'error': 'Estrutura de dados inválida. Faltam dados da moto, log ou localização.'}), 400

    moto_data = data.get('moto_data')
    log_file = data.get('log_file')
    localizacao = data.get('localizacao') 

    init_csv(log_file)
    
    timestamp = datetime.now().isoformat()
    placa = moto_data.get('placa', 'N/A')
    chassi = moto_data.get('chassi', 'N/A')
    modelo = moto_data.get('modelo', 'N/A')
    km = moto_data.get('km', 'N/A')
    contrato = moto_data.get('contrato', 'N/A')
    ocorrencia = moto_data.get('ocorrencia', 'N/A')

    try:
        with open(log_file, mode='a', newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, placa, chassi, modelo, km, contrato, ocorrencia, localizacao])
        return jsonify({'message': f'Moto {placa} armazenada com sucesso em {log_file} na localização {localizacao}!', 'data': moto_data}), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao salvar dados: {str(e)}'}), 500
