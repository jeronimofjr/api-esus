import os
from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")

def register_swagger(app: Flask):
    @app.route("/api/v1/docs/openapi.yml")
    def openapi_spec():
        return send_from_directory(os.path.abspath(DOCS_DIR), "openapi.yml")

    swagger_bp = get_swaggerui_blueprint(
        "/api/v1/docs",                    
        "/api/v1/docs/openapi.yml",  
        config={"app_name": "Desafio Painel ESUS"},
    )
    app.register_blueprint(swagger_bp, url_prefix="/api/v1/docs")