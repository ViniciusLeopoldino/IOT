# Mottu Vision – Sistema de Identificação Visual

![Status](https://img.shields.io/badge/status-Concluído-green)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Framework](https://img.shields.io/badge/Framework-Flask-black.svg)
![Computer Vision](https://img.shields.io/badge/Vision-OpenCV-orange.svg)

## 1. Descrição do Projeto
O **Mottu Vision** é um protótipo funcional que utiliza Visão Computacional para otimizar e automatizar o processo de registro de motocicletas em pátios de armazenamento. A aplicação é controlada por um menu interativo que guia o operador através de um processo de **check-in em duas etapas**: primeiro, escaneando o QR Code da motocicleta e, em seguida, o código de barras da sua localização no pátio.

## 2. Problema de Negócio
A gestão manual de frotas em grandes pátios é lenta e propensa a erros. O registro incorreto não só de dados do veículo, mas também de sua localização, pode causar grandes ineficiências logísticas, dificultando o rastreamento e a movimentação dos ativos da Mottu.

## 3. Solução Proposta
Nossa solução é um sistema de "check-in" inteligente que garante a precisão do registro através de uma verificação dupla:
1.  **Identificação do Veículo:** O operador escaneia um QR Code na moto. O sistema captura os dados e fecha a câmera.
2.  **Confirmação do Operador:** Os dados da moto são exibidos no terminal para verificação visual. O operador deve confirmar se estão corretos.
3.  **Identificação da Localização:** Após a confirmação, o sistema reativa a câmera para que o operador escaneie o código de barras da vaga ou prateleira onde a moto será armazenada.
4.  **Armazenamento:** Com as duas informações validadas, o sistema salva um registro completo no arquivo de log da sessão, associando o veículo à sua localização exata.

Essa abordagem elimina a digitação, minimiza erros e cria um registro de dados robusto e confiável.

## 4. Principais Funcionalidades
* **Check-in em Duas Etapas:** Garante a precisão ao registrar primeiro a moto e depois sua localização.
* **Confirmação do Usuário:** O processo exige a validação do operador antes de prosseguir.
* **Menu Interativo:** Controle centralizado da aplicação via terminal.
* **Backend sob Demanda:** O servidor Flask é iniciado automaticamente em segundo plano.
* **Logs Personalizáveis:** Permite nomear os arquivos de registro para cada sessão (ex: por pátio ou data).
* **Visualizador de Logs:** Ferramenta integrada para consultar os dados salvos em formato de tabela.

## 5. Arquitetura e Fluxo de Dados
O sistema opera a partir de um script principal (`main.py`) que orquestra todo o processo de check-in.

```
Usuário -> main.py (Menu no Terminal)
    |
    +-> Opção 1: Iniciar Check-in
    |   |
    |   +-> Solicita o nome do arquivo de log (ex: patio_A.csv)
    |   |
    |   +-> Inicia backend.py (em thread)
    |   |
    |   +-> Chama vision.py para ler o QR Code da MOTO
    |       |
    |       +-> Câmera abre, lê o QR, fecha e retorna os dados da moto.
    |
    +-> main.py exibe os dados e pede confirmação (s/n)
    |   |
    |   +-> Se 's', chama vision.py para ler o Código de Barras da LOCALIZAÇÃO
    |       |
    |       +-> Câmera abre, lê o código, fecha e retorna a localização.
    |
    +-> main.py envia um HTTP POST para o backend.py com { MOTO + LOCALIZAÇÃO }
        |
        +-> backend.py escreve o registro completo no arquivo 'patio_A.csv'.
```

## 6. Tecnologias Utilizadas
* **Linguagem:** Python 3
* **Visão Computacional:**
    * `opencv-python`: Captura do feed de vídeo da webcam.
    * `pyzbar`: Decodificação de QR Codes e Códigos de Barras.
* **Backend:**
    * `Flask`: Criação do microserviço para recebimento dos dados.
* **Comunicação:**
    * `requests`: Realização de chamadas HTTP para o backend.
* **Manipulação de Dados:**
    * `pandas`: Leitura e exibição formatada dos arquivos `.csv`.
* **Concorrência:**
    * `threading`: Para executar o servidor Flask em segundo plano.

## 7. Estrutura de Arquivos
```
.
├── main.py               # Ponto de entrada principal, com o menu e a lógica do fluxo.
├── vision.py             # Módulo com as funções de leitura da webcam.
├── backend.py            # Módulo com o microserviço Flask para salvar os dados.
├── requirements.txt      # Lista de dependências do projeto.
└── ...                   # Arquivos .csv serão gerados aqui durante o uso.
```

## 8. Instruções de Instalação e Execução

### Pré-requisitos
* Python 3.8 ou superior e `pip`.
* Uma webcam conectada.

### Passo 1: Configuração do Ambiente
```bash
# 1. Clone o repositório
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DA_PASTA>

# 2. Crie e ative um ambiente virtual
python -m venv venv
# Windows: venv\Scripts\activate | macOS/Linux: source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt
```

### Passo 2: Execução da Aplicação
Para iniciar o sistema, execute um único comando:
```bash
python main.py
```
Siga as instruções do menu que aparecerá no terminal.

## 9. Como Usar e Testar a Aplicação

### Materiais para Teste
Você precisará de dois códigos para a demonstração:
1.  **QR Code da Moto:** Um QR Code contendo dados em formato JSON. Exemplo:
    ```json
    {"placa": "MTO2025", "chassi": "9C2KC1670GR500001", "modelo": "Honda Pop 110i"}
    ```
2.  **Código de Barras da Vaga:** Um código de barras qualquer (pode ser outro QR Code ou um Code 128) com um texto simples. Exemplo: `R01-M01-A01-V01`

### Fluxo de Uso
1.  Execute `python main.py`.
2.  **Escolha a Opção 1** para "Fazer Check-in".
3.  **Dê um nome ao arquivo de log** (ex: `registros_hoje.csv`) e pressione Enter.
4.  A webcam abrirá. **Aponte para o QR Code da moto**. A câmera fechará automaticamente.
5.  Os dados da moto serão exibidos. **Digite `s`** para confirmar.
6.  A webcam abrirá novamente. **Aponte para o código de barras da localização**. A câmera fechará.
7.  Uma mensagem de sucesso confirmará o armazenamento.
8.  Use a **Opção 2** para visualizar o log e verificar que o registro foi salvo com a coluna "localizacao" preenchida.

## 10. Integrantes
* **RM:** 557047 **Nome:** Vinicius Leopoldino de Oliveira
* **RM:** 556834 **Nome:** Pablo Lopes Doria de Andrade
* **Curso:** Análise e Desenvolvimento de Sistemas - FIAP
* **Matéria:** Disruptive Architectures: IoT, IOB & Generative IA
