from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.models.atendimentos import Atendimento

class AtendimentoRepository:
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def find_all(self, page: int, limit: int) -> tuple[List[Atendimento], int]:
        query = self.db.query(Atendimento)
                
        return self._paginate(query, page, limit)
    
    def find_by_id(self, atendimento_id: int) -> Optional[Atendimento]:
        return self.db.query(Atendimento).filter(Atendimento.id == atendimento_id).first()
    
    def find_by_filters(self, filters: Dict[str, any], page: int, limit: int) -> List[Atendimento]:
        
        query = self.db.query(Atendimento)
        
        for key, value in filters.items():
            if hasattr(Atendimento, key):
                query = query.filter(getattr(Atendimento, key) == value)
        
        return self._paginate(query, page, limit)
    
    def find_by_unidade(self, unidade: str) -> List[Atendimento]:
        return self.db.query(Atendimento).filter(Atendimento.UNIDADE == unidade).all()
    
    def find_by_condicao_saude(self, condicao: str) -> List[Atendimento]:
        return self.db.query(Atendimento).filter(Atendimento.condicao_saude == condicao).all()
    
    def find_by_data_atendimento(self, data: str) -> List[Atendimento]:
        return self.db.query(Atendimento).filter(Atendimento.data_atendimento == data).all()
    
    def find_by_cpf_data_atendimento(self, cpf: str) -> List[Atendimento]:
        return self.db.query(Atendimento).filter(Atendimento.cpf == cpf).all()
    
    def find_by_period(self, data_inicio: str, data_fim: str) -> List[Atendimento]:
        return self.db.query(Atendimento).filter(
            and_(
                Atendimento.data_atendimento >= data_inicio,
                Atendimento.data_atendimento <= data_fim
                )).all()
    
    def count(self) -> int:    
        return self.db.query(Atendimento).count()
    
    
    def count_by_filters(self, filters: Dict[str, any]) -> int:
        
        return len(self.find_by_filters(filters))

    def count_condicao_saude(self) -> dict[str, int]:
        registros_por_condicao = (
            self.db.query(
                Atendimento.condicao_saude, 
                func.count(Atendimento.id)
            )
            .group_by(Atendimento.condicao_saude)
            .all()
            )
        
        return {condicao : total for condicao, total in registros_por_condicao}

    def count_pessoas_atendidas(self) -> int:
        return self.db.query(func.count(func.distinct(Atendimento.cpf))).scalar()
            
    def _paginate(self, query, page: int, limit: int) -> tuple[List[Atendimento], int]:
        total = query.count()

        items = (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return items, total
