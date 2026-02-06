from flask import jsonify
from marshmallow import ValidationError
from app.utils.responses import api_response

def register_error_handlers(app):
    
     
    @app.errorhandler(404)
    def handle_not_found(error):
        return api_response(
            success=False,
            error={
                "code": "RESOURCE_NOT_FOUND",
                "message": "Recurso não encontrado",
                "details": None
            },
            status_code=404
        )
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return api_response(
            success=False,
            error={
                "code": "VALIDATION_ERROR",
                "message": "Erro de validação nos dados enviados",
                "details": error.messages
            },
            status_code=400
        )
   
    @app.errorhandler(500)
    def handle_internal_error(error):
        return api_response(
            success=False,
            error={
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Erro interno do servidor",
                "details": None
            },
            status_code=500
        )

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        return api_response(
            success=False,
            error={
                "code": "UNEXPECTED_ERROR",
                "message": "Erro inesperado no servidor",
                "details": None
            },
            status_code=500
        )
