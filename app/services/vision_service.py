import cv2
from ultralytics import YOLO
import os

# Caminho para o SEU modelo treinado
MODEL_PATH = os.path.join("saves", "models", "modelv0.5.pt")

# Carrega o seu modelo customizado
# Adicionamos weights_only=False para garantir o carregamento do seu .pt antigo
model = YOLO(MODEL_PATH) 

def gerar_frames_camera():
    """Gerador de frames usando o modelo OunceAI v0.5"""
    camera = cv2.VideoCapture(0) # Use 0 para webcam física

    if not camera.isOpened():
        print("❌ Câmera não detectada. Verifique as permissões.")
        return

    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # 3. Rodar detecção com o seu modelo
        results = model(frame, conf=0.5, verbose=False)
        
        # Desenha as caixas e nomes das classes no frame
        annotated_frame = results[0].plot()

        # Codifica para exibir no navegador
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    camera.release()