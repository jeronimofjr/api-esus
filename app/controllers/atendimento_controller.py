from flask import Blueprint, request
import math
from app.services.atendimento_service import AtendimentoService
from app.utils.responses import api_response
from app.schemas.atendimento_schema import AtendimentoSchema, FiltrosAtendimentoSchema, PeriodoAtendimentoSchema

atendimento_bp = Blueprint('atendimentos', __name__)

class AtendimentoController:
    
    @atendimento_bp.route('/atendimentos', methods=['GET'])
    def get_atendimentos():
        
        filtro_schema = FiltrosAtendimentoSchema()
        
        filters =  filtro_schema.load(request.args.to_dict())
        
        page = filters.pop("page")
        limit = filters.pop("limit")

        service = AtendimentoService()
        
        if any(filters.values()):
            atendimentos, total = service.get_atendimentos_by_filters(filters, page, limit)
        else: 
            atendimentos, total = service.get_all_atendimentos(page, limit)
        
        total_pages = math.ceil(total/limit)
        
        if not atendimentos:
            return api_response(success=True, 
                            data={"atendimentos" : []},
                            total_items=0,
                            status_code=200)
        
        atendimento_schema = AtendimentoSchema()
        atendimentos = atendimento_schema.dump(atendimentos, many=True)
        
        return api_response(success=True, 
                            data={"atendimentos" : atendimentos},
                            total_items=total,
                            pagination={
                              "page" : page,
                              "limit" : limit,
                              "total_pages" : total_pages  
                            },
                            status_code=200)
            

    @atendimento_bp.route('/atendimentos/<int:atendimento_id>', methods=['GET'])
    def get_atendimento_by_id(atendimento_id: int):
        
        service = AtendimentoService()
        
        atendimento = service.get_atendimento_by_id(atendimento_id)
        
        if atendimento is None:
            return api_response(
                success=False,
                error="Atendimento not found",
                total_items=0,
                status_code=404
            )
        
        return api_response(success=True,
                            data={"atendimento" : atendimento},
                            total_items=1,
                            status_code=200)
    

        
    @atendimento_bp.route("/atendimentos/periodo", methods=['GET'])
    def get_atendimentos_by_period():
        
        schema = PeriodoAtendimentoSchema()
        
        periodo_schema = schema.load(request.args.to_dict())
        
        service = AtendimentoService()
        
        data_inicio = periodo_schema.pop("data_inicio")
        data_fim = periodo_schema.pop("data_fim")
        
        atendimentos = service.get_atendimentos_by_period(data_inicio, data_fim)

        if not atendimentos:
             return api_response(success=True, 
                            data={"atendimentos" : []},
                            total_items=0,
                            status_code=404)
        
        return api_response(success=True, 
                            data={"atendimentos" : atendimentos},
                            total_items=len(atendimentos),
                            status_code=200)
        
    @atendimento_bp.route("/atendimentos/stats", methods=['GET'])
    def stats():
        service = AtendimentoService()
        
        stats = service.get_statistics()
        
        return api_response(success=True, 
                            data=stats,
                            status_code=200)
        
          
