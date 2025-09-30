import cv2
from pyzbar.pyzbar import decode
import numpy as np
import json
from ultralytics import YOLO
import requests

# Carregar o modelo YOLOv8 pré-treinado (usaremos o 'n' que é mais leve)
model = YOLO('yolov8n.pt')

# URL do backend Flask
BACKEND_URL = "http://127.0.0.1:5000/armazenar_moto"

def ler_qr_da_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro: Não foi possível abrir a câmera.")
        return

    print("Aguardando detecção de QR Code... Pressione 'q' para sair.")

    # Variável para controlar o último QR Code lido e evitar duplicatas
    last_sent_placa = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Inverte o frame horizontalmente para efeito de espelho
        frame = cv2.flip(frame, 1)

        # Usamos pyzbar para decodificar todos os QR Codes no frame
        barcodes = decode(frame)
        
        qr_code_found_this_frame = False
        for barcode in barcodes:
            qr_code_found_this_frame = True
            qr_data = barcode.data.decode('utf-8')

            # Desenha o contorno do QR Code detectado
            pontos = np.array([barcode.polygon], np.int32)
            pontos = pontos.reshape((-1, 1, 2))
            cv2.polylines(frame, [pontos], True, (0, 255, 0), 3) # Verde para QR Code

            try:
                dados_moto = json.loads(qr_data)
                placa_atual = dados_moto.get('placa')

                # --- LÓGICA ANTI-DUPLICATAS ---
                # Apenas processa se a placa for nova
                if placa_atual and placa_atual != last_sent_placa:
                    print(f"Novo QR Code detectado! Placa: {placa_atual}. Enviando para o backend...")
                    
                    try:
                        response = requests.post(BACKEND_URL, json=dados_moto)
                        if response.status_code == 200:
                            print(f"✅ Sucesso! Dados enviados: {dados_moto}")
                            # Atualiza a última placa enviada para não repetir
                            last_sent_placa = placa_atual
                        else:
                            print(f"❌ Erro no backend: {response.status_code} - {response.text}")
                            # Não atualiza a última placa, para tentar de novo
                            last_sent_placa = None

                    except requests.exceptions.ConnectionError:
                        print("❌ Erro de conexão. Verifique se o backend (backend.py) está rodando.")
                        last_sent_placa = None
                
                # Feedback visual
                if last_sent_placa == placa_atual:
                    cv2.putText(frame, "MOTO JA ARMAZENADA!", (barcode.rect.left, barcode.rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
                else:
                    cv2.putText(frame, "Lendo QR Code...", (barcode.rect.left, barcode.rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)


            except (json.JSONDecodeError, KeyError):
                # Caso o QR Code não seja um JSON válido com a chave 'placa'
                cv2.putText(frame, "QR INVALIDO", (barcode.rect.left, barcode.rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                last_sent_placa = None # Reseta para permitir nova leitura
        
        # Se nenhum QR Code for detectado no frame, reseta o controle
        if not qr_code_found_this_frame:
            last_sent_placa = None


        cv2.imshow("Mottu Vision - Leitor de QR Code", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    ler_qr_da_camera()