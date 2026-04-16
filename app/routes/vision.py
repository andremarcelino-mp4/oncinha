from flask import Blueprint, Response, render_template
from app.services.vision_service import gerar_frames_camera

vision_bp = Blueprint('vision', __name__)

@vision_bp.route('/stream')
def video_stream():
    """Rota que envia o fluxo de dados da câmera"""
    return Response(gerar_frames_camera(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@vision_bp.route('/monitor')
def monitor():
    """Página que exibe a câmera"""
    return render_template('vision.html')