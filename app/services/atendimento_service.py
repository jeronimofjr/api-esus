from typing import List, Dict, Optional
from app.repositories.atendimento_repository import AtendimentoRepository
from app.config.database import db_config

class AtendimentoService:
    
    def __init__(self):
        self.db_session = db_config.get_session()
        self.repository = AtendimentoRepository(self.db_session)
        
    def get_all_atendimentos(self, page: int, limit: int) -> tuple[List[Dict], int]:
        atendimentos, total = self.repository.find_all(page, limit)
        
        return [atendimento.to_dict() for atendimento in atendimentos], total
    
    def get_atendimento_by_id(self, atendimento_id: int) -> Optional[Dict]:
        atendimento = self.repository.find_by_id(atendimento_id)
        
        return atendimento.to_dict() if atendimento else None
    
    def get_atendimentos_by_filters(self, filters: Dict[str, any], page: int, limit: int) -> tuple[List[Dict], int]:
        
        filters_ = {k: v for k, v in filters.items() if v is not None and v != ''}
        
        field_mapping = {
                'unidade': 'unidade',
                'condicao_saude': 'condicao_saude',
                'data_atendimento': 'data_atendimento'
        }
        
        mapped_filters = {}
        for key, value in filters_.items():
            if key in field_mapping:
                    mapped_filters[field_mapping[key]] = value
        
        atendimentos, total = self.repository.find_by_filters(mapped_filters, page, limit)
        
        return [atendimento.to_dict() for atendimento in atendimentos], total
    
    
    def get_statistics(self) -> Dict[str, int]:
         
         total_atendimentos = self.repository.count()
         total_registros_por_condicao = self.repository.count_condicao_saude()
         total_pessoas_atendidas = self.repository.count_pessoas_atendidas()
         
         return {"total_atendimentos" : total_atendimentos, 
                 "atendimentos_por_condicao_saude" : total_registros_por_condicao, 
                 "total_pessoas_unicas" : total_pessoas_atendidas}
     
    def get_atendimento_by_unidade(self, unidade: str) -> List[Dict]:
        
        atendimentos = self.repository.find_by_unidade(unidade)
        
        return [atendimento.to_dict() for atendimento in atendimentos]

    def get_atendimentos_by_cpf(self, cpf: str) -> Dict:
        
        atendimentos = self.repository.find_by_cpf_data_atendimento(cpf)
        
        return [atendimento.to_dict() for atendimento in atendimentos]
    
    def get_atendimentos_by_period(self, data_inicio: str, data_fim: str) -> List[Dict]:
        
        atendimentos = self.repository.find_by_period(data_inicio, data_fim)
        
        return [atendimento.to_dict() for atendimento in atendimentos]

    def __del__(self):
        if hasattr(self, 'db_session'):
            self.db_session.close()