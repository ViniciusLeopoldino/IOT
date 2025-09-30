import cv2
from pyzbar.pyzbar import decode
import numpy as np
import json

def find_one_qr_code():
    """Abre a webcam, procura por um QR Code de MOTO (JSON), fecha e retorna os dados."""
    WINDOW_NAME = "Mottu Vision - Aponte para o QR Code da MOTO"
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro: Não foi possível abrir a câmera.")
        return None

    cv2.namedWindow(WINDOW_NAME)
    print("\nINFO: Câmera aberta. Procurando por QR Code da MOTO...")
    
    dados_moto = None
    while True:
        # ... (código desta função permanece o mesmo da versão anterior)
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, 1)
        barcodes = decode(frame)
        for barcode in barcodes:
            pontos = np.array([barcode.polygon], np.int32).reshape((-1, 1, 2))
            cv2.polylines(frame, [pontos], True, (0, 255, 0), 3)
            try:
                dados_moto = json.loads(barcode.data.decode('utf-8'))
                if 'placa' in dados_moto:
                    print(f"SUCCESS: QR Code válido encontrado! Placa: {dados_moto['placa']}")
                    break 
            except (json.JSONDecodeError, KeyError):
                cv2.putText(frame, "QR MOTO INVALIDO", (barcode.rect.left, barcode.rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                continue
        cv2.imshow(WINDOW_NAME, frame)
        if dados_moto: break
        if cv2.waitKey(1) == ord('q') or cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            print("INFO: Leitura cancelada pelo usuário.")
            dados_moto = None
            break
    cap.release()
    cv2.destroyAllWindows()
    return dados_moto

def find_location_code():
    """Abre a webcam, procura por qualquer código de barras de LOCALIZAÇÃO (texto), fecha e retorna os dados."""
    WINDOW_NAME = "Mottu Vision - Aponte para o Codigo de Barras da VAGA"
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro: Não foi possível abrir a câmera.")
        return None

    cv2.namedWindow(WINDOW_NAME)
    print("\nINFO: Câmera aberta. Procurando por Código de Barras da LOCALIZACAO...")
    
    location_code = None
    while True:
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, 1)
        barcodes = decode(frame)
        
        for barcode in barcodes:
            # Para a localização, qualquer código de barras com texto serve.
            location_code = barcode.data.decode('utf-8')
            if location_code:
                print(f"SUCCESS: Código de localização lido: {location_code}")
                # Desenha o contorno para dar feedback
                pontos = np.array([barcode.polygon], np.int32).reshape((-1, 1, 2))
                cv2.polylines(frame, [pontos], True, (0, 255, 255), 3) # Ciano para localização
                cv2.imshow(WINDOW_NAME, frame)
                cv2.waitKey(500) # Mostra o contorno por meio segundo
                break

        cv2.imshow(WINDOW_NAME, frame)
        if location_code: break
        if cv2.waitKey(1) == ord('q') or cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            print("INFO: Leitura da localização cancelada.")
            location_code = None
            break
            
    cap.release()
    cv2.destroyAllWindows()
    return location_code
