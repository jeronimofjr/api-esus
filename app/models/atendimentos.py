from sqlalchemy import Column, String, Date, Integer
from app.config.database import Base


class Atendimento(Base):
    __tablename__ = "atendimentos"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    nascimento = Column(String)
    cns = Column(String)
    cpf = Column(String)
    unidade = Column(String)
    data_atendimento = Column(Date)
    condicao_saude = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "nascimento": self.nascimento,
            "cns": self.cns,
            "cpf": self.cpf,
            "unidade": self.unidade,
            "data_atendimento": (
                str(self.data_atendimento) if self.data_atendimento else None
            ),
            "condicao_saude": self.condicao_saude,
        }

    def __repr__(self):
        return (
            f"<Atendimento(id={self.id}, "
            f"nome='{self.nome}', "
            f"data='{self.data_atendimento}')>"
        )