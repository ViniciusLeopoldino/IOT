# Mottu Vision – Sistema de Identificação Visual de Motocicletas

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Framework](https://img.shields.io/badge/Framework-Flask-green.svg)
![Computer Vision](https://img.shields.io/badge/Vision-OpenCV%20%7C%20YOLOv8-orange.svg)

O **Mottu Vision** é um protótipo funcional que utiliza Visão Computacional para automatizar a identificação e o registro de motocicletas em pátios de armazenamento. O sistema detecta motocicletas em um feed de vídeo ou imagem, localiza e decodifica um QR Code associado a ela e persiste os dados em um sistema de backend.

---

## 🎯 Problema de Negócio

A gestão manual de frotas de motocicletas em grandes pátios é um processo lento, caro e sujeito a erros humanos. A necessidade de digitar informações como placa, chassi e contrato para cada veículo consome tempo produtivo e pode levar a registros inconsistentes, dificultando a localização e o gerenciamento logístico dos ativos da empresa Mottu.

## 💡 Solução Proposta

Implementamos uma solução de Visão Computacional que automatiza o processo de "check-in" das motocicletas. Utilizando o modelo de detecção de objetos **YOLOv8**, o sistema identifica motos em tempo real. Em seguida, dentro da área da moto detectada, um leitor de QR Code (`pyzbar`) extrai os dados contidos em uma etiqueta, que são enviados via requisição HTTP para um backend que armazena as informações de forma persistente.

---

## 🛠️ Arquitetura do Sistema

O projeto é dividido em dois componentes principais que se comunicam via API REST:

1.  **Frontend (Visão Computacional - `mottu_vision_*.py`)**
    * Responsável por capturar e processar as imagens (de câmera, vídeo ou arquivo).
    * Utiliza o modelo **YOLOv8** para detectar a classe "motorcycle".
    * Para cada moto detectada, delimita uma Região de Interesse (ROI).
    * Usa a biblioteca **pyzbar** para escanear a ROI em busca de QR Codes.
    * Ao encontrar e decodificar um QR Code contendo um JSON válido, utiliza a biblioteca **requests** para enviar os dados para o backend.
    * Fornece feedback visual em tempo real, desenhando caixas de detecção e status na imagem.

2.  **Backend (API de Armazenamento - `backend.py`)**
    * Construído com **Flask**, um microframework Python.
    * Expõe um único endpoint: `/armazenar_moto` (aceita requisições `POST`).
    * Recebe os dados da moto em formato JSON.
    * Adiciona um `timestamp` ao registro.
    * Salva (persiste) os dados de forma estruturada em um arquivo **`log_motos.csv`**, funcionando como um banco de dados simplificado.
    * Retorna uma resposta de sucesso (`HTTP 200`) ou erro para o frontend.

### Fluxo de Dados
```
1. Imagem de entrada --> [mottu_vision_image.py]
                               |
2. Deteccao de Moto (YOLOv8) --> ROI
                               |
3. Leitura de QR Code (pyzbar) --> JSON com dados da moto
                               |
4. HTTP POST Request ----------> [backend.py @ /armazenar_moto]
                                                    |
5. Processamento (Flask) ---------------------------> Persistencia em log_motos.csv
                                                    |
6. HTTP 200 OK Response <------ [backend.py]
       |
7. Exibicao de "SUCESSO" na imagem <-- [mottu_vision_image.py]
```

---

## 🚀 Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Visão Computacional:**
    * `ultralytics`: Para o modelo de detecção de objetos YOLOv8.
    * `opencv-python`: Para manipulação de imagem e vídeo.
    * `pyzbar`: Para decodificação de códigos de barra e QR Codes.
    * `numpy`: Para operações numéricas e manipulação de arrays.
* **Backend:**
    * `Flask`: Para a criação da API REST.
* **Comunicação:**
    * `requests`: Para realizar chamadas HTTP do frontend para o backend.

---

## 📂 Estrutura de Arquivos

```
.
├── backend.py                # Servidor Flask que armazena os dados
├── mottu_vision.py           # Script principal para detecção via WEBCAM
├── mottu_vision_image.py     # Script modificado para detecção em IMAGEM ESTÁTICA
├── requirements.txt          # Lista de dependências do projeto
├── log_motos.csv             # Arquivo de log onde os dados são salvos 
├── imgs/
│   └── moto_com_qr.jpg       # Imagem de exemplo para teste
├── resultados/
│   └── resultado_detecao.jpg # Imagem de saída com as detecções
└── README.md                 # Este arquivo
```

---

## ▶️ Como Executar o Projeto

Siga os passos abaixo para configurar e rodar o ambiente localmente.

### 1. Pré-requisitos
* Python 3.8 ou superior
* `pip` (gerenciador de pacotes do Python)

### 2. Clonar o Repositório
```bash
git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
cd SEU_REPOSITORIO
```

### 3. Instalar as Dependências
É altamente recomendável criar um ambiente virtual.

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Instalar as bibliotecas necessárias
pip install -r requirements.txt
```

### 4. Executar o Backend
O backend precisa estar rodando para receber e salvar os dados.

```bash
python backend.py
```
O terminal deve indicar que o servidor está rodando em `http://127.0.0.1:5000`.

### 5. Executar o Frontend (Visão Computacional)

Abra **um novo terminal**, ative o ambiente virtual novamente e escolha uma das opções abaixo:

**Opção A: Testar com uma Imagem Estática (Recomendado)**
Certifique-se de ter a imagem `imgs/moto_com_qr.jpg` configurada.

```bash
python mottu_vision_image.py
```
Uma janela aparecerá com o resultado da detecção.

**Opção B: Testar com a Webcam**
```bash
python mottu_vision.py
```
Aponte sua webcam para um QR Code para iniciar a detecção.

### 6. Como Gerar um QR Code para Teste
Use um gerador de QR Code online (como o [QR Code Generator](https://www.qr-code-generator.com/)) e insira um texto no formato JSON como o exemplo abaixo:

```json
{
  "placa": "MTO2W23",
  "chassi": "9C2KC1670GR500001",
  "modelo": "Honda Pop 110i",
  "km": "5300",
  "contrato": "987654321",
  "ocorrencia": "Arranhao no tanque"
}
```

---

## 🎥 Vídeo de Demonstração

Assista ao protótipo no YouTube:  https://www.youtube.com/watch?v=ZxqEnVOUHW

---

## 👨‍💻 Integrantes

* **RM:** 557047 **Nome:** Vinicius Leopoldino de Oliveira
* **RM:** 556834 **Nome:** Pablo Lopes Doria de Andrade
* **Curso:** Análise e Desenvolvimento de Sistemas - FIAP
* **Matéria:** Disruptive Architectures: IoT, IOB & Generative IA
