from flask import Flask
from flask_cors import CORS

from .controllers.atendimento_controller import atendimento_bp
from .controllers.system_controller import system_bp
from .utils.error_handlers import register_error_handlers
from .utils.swagger import register_swagger

def create_app():
    app = Flask(__name__)
    
    CORS(app)
    
    from .config.database import db_config
    
    with app.app_context():
        db_config.init_database()
    
    register_error_handlers(app)
    register_swagger(app)
    
    app.register_blueprint(atendimento_bp, url_prefix='/api/v1')
    app.register_blueprint(system_bp, url_prefix='/api/v1')
    
    
    return app