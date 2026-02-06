from flask import Blueprint, send_file, jsonify

system_bp = Blueprint("system", __name__)

@system_bp.route("/info", methods=["GET"])
def api_info():
    return jsonify({
        "name": "Painel SUS - API REST",
        "version": "2.0",
        "status": "online",
        "environment": "development",
        "endpoints": {
            "atendimentos": "/api/v1/atendimentos",
            "atendimento_by_id": "/api/v1/atendimentos/unidade/<atendimento_id>",
            "statistics": "/api/v1/atendimentos/stats"
        },
        "docs": "/api/v1/docs"
    }), 200


@system_bp.route("/health-check", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "service": "Painel SUS - API",
        "version": "2.0.0"
    }), 200


@system_bp.route("/docs/openapi.yml", methods=["GET"])
def openapi_spec():
    return send_file("/docs/openapi.yml")