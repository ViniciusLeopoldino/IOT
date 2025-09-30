# Mottu Vision – Sistema de Identificação Visual de Motocicletas

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Framework](https://img.shields.io/badge/Framework-Flask-green.svg)
![Computer Vision](https://img.shields.io/badge/Vision-OpenCV%20%7C%20YOLOv8-orange.svg)

O **Mottu Vision** é um protótipo funcional que utiliza Visão Computacional para automatizar a identificação e o registro de motocicletas em pátios de armazenamento. O sistema utiliza a webcam para ler QR Codes contendo os dados de uma moto e os persiste em um sistema de backend.

---

## 🎯 Problema de Negócio

A gestão manual de frotas de motocicletas em grandes pátios é um processo lento, caro e sujeito a erros humanos. A necessidade de digitar informações como placa, chassi e contrato para cada veículo consome tempo produtivo e pode levar a registros inconsistentes, dificultando a localização e o gerenciamento logístico dos ativos da Mottu.

## 💡 Solução Proposta

Implementamos uma solução de Visão Computacional que automatiza o processo de "check-in" das motocicletas. Utilizando a webcam de um dispositivo (como um celular ou tablet), o sistema localiza e decodifica um QR Code afixado na motocicleta. Os dados extraídos são enviados via requisição HTTP para um backend simples que armazena as informações de forma persistente em um arquivo CSV, que funciona como um log de registros.

---

## 🏛️ Arquitetura do Sistema

O projeto é dividido em dois componentes principais que se comunicam via API REST:

1.  **Frontend (Visão Computacional - `mottu_vision.py`)**
    * Responsável por capturar o feed da webcam usando **OpenCV**.
    * Utiliza a biblioteca **pyzbar** para escanear o vídeo em tempo real em busca de QR Codes.
    * Ao encontrar e decodificar um QR Code contendo um JSON válido, utiliza a biblioteca **requests** para enviar os dados para o backend.
    * Possui uma lógica para evitar o envio de registros duplicados em sequência.
    * Fornece feedback visual em tempo real, desenhando contornos e status na janela de vídeo.

2.  **Backend (API de Armazenamento - `backend.py`)**
    * Construído com **Flask**, um microframework Python.
    * Expõe um único endpoint: `/armazenar_moto` (aceita requisições `POST`).
    * Recebe os dados da moto em formato JSON, adiciona um `timestamp` ao registro.
    * Salva (persiste) os dados de forma estruturada em um arquivo **`log_motos.csv`**, funcionando como um banco de dados simplificado.
    * Retorna uma resposta de sucesso ou erro para o frontend.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Visão Computacional:**
    * `opencv-python`: Para captura e manipulação de vídeo da webcam.
    * `pyzbar`: Para decodificação de códigos de barra e QR Codes.
    * `numpy`: Para operações numéricas.
* **Backend:**
    * `Flask`: Para a criação da API REST.
* **Comunicação:**
    * `requests`: Para realizar chamadas HTTP do frontend para o backend.
* **Detecção de Objetos (Opcional/Estudo):**
    * `ultralytics`: O modelo YOLOv8 foi utilizado em fases iniciais de estudo, mas a versão final foca na leitura de QR Codes para simplicidade e precisão.

---

## ▶️ Como Executar o Projeto

Siga os passos abaixo para configurar e rodar o ambiente localmente.

### 1. Pré-requisitos
* Python 3.8 ou superior
* `pip` (gerenciador de pacotes do Python)
* Uma webcam conectada ao computador.

### 2. Instalação
```bash
# Clone este repositório
git clone https://github.com/ViniciusLeopoldino/IOT.git
cd IOT

# Crie e ative um ambiente virtual (altamente recomendado)
python -m venv venv
# No Windows: venv\Scripts\activate
# No macOS/Linux: source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 3. Execução dos Serviços (em 2 Terminais)

* **Terminal 1: Inicie o Backend**
    O backend precisa estar rodando para receber e salvar os dados.
    ```bash
    python backend.py
    ```
    O terminal deve indicar que o servidor está rodando em `http://127.0.0.1:5000`.

* **Terminal 2: Inicie o Frontend (Visão Computacional)**
    Abra um **novo terminal** (e ative o ambiente virtual novamente).
    ```bash
    python mottu_vision.py
    ```
    Uma janela do OpenCV será aberta, exibindo o feed da sua webcam.

### 4. Como Testar
1.  **Gere um QR Code:** Use um gerador online (como o [QR Code Generator](https://www.qr-code-generator.com/)) e insira um texto em formato JSON como no exemplo abaixo:
    ```json
    {
      "placa": "MTO2025",
      "chassi": "9C2KC1670GR500001",
      "modelo": "Honda Pop 110i",
      "km": "5300",
      "contrato": "987654321",
      "ocorrencia": "Arranhao no tanque"
    }
    ```
2.  **Aponte a Webcam:** Mostre o QR Code (na tela do seu celular ou impresso) para a webcam.
3.  **Observe:** O sistema irá destacar o QR Code, enviar os dados, e o terminal do backend mostrará a requisição recebida. O arquivo `log_motos.csv` será atualizado com uma nova linha.

---

## 👨‍💻 Integrantes

* **RM:** 557047 **Nome:** Vinicius Leopoldino de Oliveira
* **RM:** 556834 **Nome:** Pablo Lopes Doria de Andrade
* **Curso:** Análise e Desenvolvimento de Sistemas - FIAP
* **Matéria:** Disruptive Architectures: IoT, IOB & Generative IA