from flask import Flask, redirect, url_for

def create_app():
    # Inicializa o Flask informando onde estão os templates
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Importa as rotas (Blueprints)
    from app.routes.inventory import inventory_bp
    from app.routes.vision import vision_bp
    # from app.routes.chat import chat_bp
    # from app.routes.marketing import marketing_bp

    # Registra as rotas no aplicativo
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(vision_bp, url_prefix='/vision')
    
    # Rota raiz - Redireciona direto para o Dashboard
    @app.route('/')
    def index():
        return redirect(url_for('inventory.dashboard'))

    return app