# Instruções de Execução

Para executar o sistema Mottu Vision, siga os passos abaixo:

## 1. Instalação das Dependências

Certifique-se de ter o Python 3 instalado em seu sistema. Em seguida, instale as bibliotecas necessárias utilizando o `pip` e o arquivo `requirements.txt` fornecido:

```bash
pip install -r requirements.txt
```

## 2. Executar o Backend

Abra um terminal e navegue até o diretório `challenge_iot-main`. Em seguida, execute o script `backend.py`:

```bash
python backend.py
```

O backend será iniciado e estará aguardando requisições na porta `5000` (http://127.0.0.1:5000).

## 3. Executar o Frontend (Visão Computacional)

Abra **outro** terminal e navegue até o diretório `challenge_iot-main`. Em seguida, execute o script `mottu_vision.py`:

```bash
python mottu_vision.py
```

Uma janela do OpenCV será aberta, exibindo o feed da sua webcam. O sistema irá:

1.  Detectar motocicletas usando o modelo YOLOv8.
2.  Dentro das caixas de detecção das motos, procurar por QR Codes.
3.  Se um QR Code for detectado e contiver dados JSON válidos, ele tentará enviar esses dados para o backend.
4.  Exibirá mensagens de status na tela (MOTO ARMAZENADA! ou ERRO).

## 4. Testar com QR Code

Aponte sua webcam para um QR Code com conteúdo JSON similar ao exemplo abaixo:

```json
{
  "placa": "ABC1234",
  "chassi": "9C2KC1670GR500001",
  "modelo": "Honda CG 160",
  "km": "12400",
  "contrato": "87654321",
  "ocorrencia": "Nenhuma"
}
```

Você pode gerar QR Codes personalizados em sites como [QR Code Generator](https://www.qr-code-generator.com/).

Certifique-se de que o QR Code esteja visível e bem iluminado para uma detecção eficaz. O sistema destacará a moto detectada e o QR Code lido, além de informar o status do armazenamento. 
armazenamento.

