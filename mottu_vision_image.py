import cv2
from pyzbar.pyzbar import decode
import numpy as np
import json
from ultralytics import YOLO
import requests
import os

# --- CONFIGURAÇÕES ---
# Carregar o modelo YOLOv8 pré-treinado
model = YOLO('yolov8n.pt')

# URL do backend Flask
BACKEND_URL = "http://127.0.0.1:5000/armazenar_moto"

# Caminho para a imagem de entrada
IMAGE_PATH = 'imgs/moto_com_qr.jpg'

# Pasta para salvar a imagem de resultado
OUTPUT_DIR = 'resultados'
os.makedirs(OUTPUT_DIR, exist_ok=True)
# --- FIM DAS CONFIGURAÇÕES ---

def processar_imagem(image_path):
    """
    Carrega uma imagem, detecta motos e QR Codes, envia os dados para o backend
    e exibe o resultado.
    """
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Erro: Não foi possível carregar a imagem em '{image_path}'")
        return

    print(f"Processando a imagem: {image_path}")
    
    # Realizar detecção de objetos com YOLO
    results = model(frame, stream=True)

    # Itera sobre os resultados da detecção
    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            # Verifica se o objeto detectado é uma motocicleta
            if model.names[cls] == 'motorcycle':
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Desenha a caixa de detecção da moto (azul)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, 'Moto Detectada', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

                # Define a Região de Interesse (ROI) para buscar o QR Code
                roi = frame[y1:y2, x1:x2]

                # Detecta e decodifica QR Codes dentro da ROI
                for barcode in decode(roi):
                    # Desenha o contorno do QR Code (verde)
                    pontos = np.array([barcode.polygon], np.int32)
                    pontos[:, :, 0] += x1
                    pontos[:, :, 1] += y1
                    pontos = pontos.reshape((-1, 1, 2))
                    cv2.polylines(frame, [pontos], True, (0, 255, 0), 3)

                    qr_data = barcode.data.decode('utf-8')
                    texto_display = "QR Lido"
                    
                    try:
                        dados_moto = json.loads(qr_data)
                        texto_display = f"Placa: {dados_moto.get('placa', 'N/A')}"

                        # Enviar dados para o backend
                        try:
                            response = requests.post(BACKEND_URL, json=dados_moto)
                            if response.status_code == 200:
                                print(f"✅ Sucesso! Dados enviados para o backend: {dados_moto}")
                                cv2.putText(frame, "MOTO ARMAZENADA!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                            else:
                                print(f"❌ Erro no backend: {response.status_code} - {response.text}")
                                cv2.putText(frame, "ERRO NO BACKEND!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                        
                        except requests.exceptions.ConnectionError:
                            print("❌ Erro de conexão. Verifique se o backend (backend.py) está em execução.")
                            cv2.putText(frame, "BACKEND OFFLINE!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

                    except json.JSONDecodeError:
                        print(f"❌ QR Code lido não contém um JSON válido: {qr_data}")
                        texto_display = "QR com JSON Inválido"
                    
                    # Escreve o texto com os dados do QR Code
                    x_qr, y_qr, _, _ = barcode.rect
                    cv2.putText(frame, texto_display, (x_qr + x1, y_qr + y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Salva a imagem com as detecções
    output_path = os.path.join(OUTPUT_DIR, 'resultado_detecao.jpg')
    cv2.imwrite(output_path, frame)
    print(f"✅ Imagem de resultado salva em: {output_path}")

    # Exibe a imagem final
    cv2.imshow("Mottu Vision - Resultado da Deteccao", frame)
    print("Pressione qualquer tecla para fechar a janela da imagem.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    processar_imagem(IMAGE_PATH)