
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import json
from ultralytics import YOLO
import requests
import time

# Carregar o modelo YOLOv8 pré-treinado
model = YOLO('yolov8n.pt')  # Você pode usar 'yolov8n.pt', 'yolov8s.pt', etc.

# URL do backend Flask
BACKEND_URL = "http://127.0.0.1:5000/armazenar_moto"

def ler_qr_da_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro: Não foi possível abrir a câmera.")
        return

    print("Aguardando detecção de motos e leitura de QR Code... Pressione 'q' para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Realizar detecção de objetos com YOLO
        results = model(frame, stream=True)

        moto_detectada = False
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])
                # Supondo que 'moto' ou 'motocicleta' seja uma das classes detectadas
                # Você pode precisar ajustar o ID da classe dependendo do modelo YOLO
                # Para YOLOv8, 'motorcycle' geralmente é a classe 3
                if model.names[cls] == 'motorcycle':  # ou 'moto', 'motorbike'
                    moto_detectada = True
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # Desenhar caixa de detecção do YOLO
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2) # Azul para YOLO
                    cv2.putText(frame, 'Moto', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

                    # Definir ROI para busca de QR Code
                    roi = frame[y1:y2, x1:x2]

                    # Detectar e decodificar QR Codes dentro da ROI
                    for barcode in decode(roi):
                        pontos = np.array([barcode.polygon], np.int32)
                        # Ajustar coordenadas dos pontos do QR para o frame original
                        pontos[:, :, 0] += x1
                        pontos[:, :, 1] += y1
                        pontos = pontos.reshape((-1, 1, 2))
                        cv2.polylines(frame, [pontos], True, (0, 255, 0), 3) # Verde para QR Code

                        qr_data = barcode.data.decode('utf-8')
                        try:
                            dados_moto = json.loads(qr_data)
                            texto_display = f"{dados_moto.get('placa', 'N/A')} - {dados_moto.get('modelo', 'N/A')}"

                            # Enviar dados para o backend
                            try:
                                response = requests.post(BACKEND_URL, json=dados_moto)
                                if response.status_code == 200:
                                    print(f"✅ QR Code Detectado e Dados Enviados: {dados_moto}")
                                    cv2.putText(frame, "MOTO ARMAZENADA!", (x1, y2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                else:
                                    print(f"❌ Erro ao enviar dados: {response.status_code} - {response.text}")
                                    cv2.putText(frame, "ERRO ARMAZENAMENTO!", (x1, y2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                            except requests.exceptions.ConnectionError:
                                print("❌ Erro de conexão com o backend. Verifique se o backend está rodando.")
                                cv2.putText(frame, "BACKEND OFFLINE!", (x1, y2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                        except json.JSONDecodeError:
                            print(f"❌ QR Code lido não é um JSON válido: {qr_data}")
                            texto_display = "QR Inválido"
                        except Exception as e:
                            print(f"❌ Erro ao processar QR Code: {e}")
                            texto_display = "Erro QR"

                        x_qr, y_qr, w_qr, h_qr = barcode.rect
                        cv2.putText(frame, texto_display, (x_qr + x1, y_qr + y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Mottu Vision - Leitor QR", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    ler_qr_da_camera()


