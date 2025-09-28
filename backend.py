
from flask import Flask, request, jsonify
import csv
import os
from datetime import datetime

app = Flask(__name__)

CSV_FILE = 'log_motos.csv'

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(['timestamp', 'placa', 'chassi', 'modelo', 'km', 'contrato', 'ocorrencia'])

@app.route('/armazenar_moto', methods=['POST'])
def armazenar_moto():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Nenhum dado JSON recebido'}), 400

    timestamp = datetime.now().isoformat()
    placa = data.get('placa', 'N/A')
    chassi = data.get('chassi', 'N/A')
    modelo = data.get('modelo', 'N/A')
    km = data.get('km', 'N/A')
    contrato = data.get('contrato', 'N/A')
    ocorrencia = data.get('ocorrencia', 'N/A')

    try:
        with open(CSV_FILE, mode='a', newline="") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, placa, chassi, modelo, km, contrato, ocorrencia])
        return jsonify({'message': 'Moto armazenada com sucesso!', 'data': data}), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao salvar dados: {str(e)}'}), 500

if __name__ == '__main__':
    init_csv()
    app.run(debug=True, host='0.0.0.0', port=5000)


