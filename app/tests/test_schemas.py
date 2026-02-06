import pytest
from marshmallow import ValidationError
from app.schemas.atendimento_schema import (
    AtendimentoSchema,
    FiltrosAtendimentoSchema,
    PeriodoAtendimentoSchema
)

# Testes do AtendimentoSchema

def test_atendimento_schema_mascara_cpf():
    dados = {"id" : 1, "cpf" : "12345678987", "nome" : "Teste"}
    
    resultado = AtendimentoSchema().dump(dados)
    
    assert resultado["cpf"] == "***.***.***-87"

def test_atendimento_schema_cpf_none():
    dados = {"id" : 1, "cpf" : None, "nome" : "Teste"}
    
    resultado = AtendimentoSchema().dump(dados)
    
    assert resultado["cpf"]  is None

# Testes do FiltrosAtendimentoSchema

def test_filtros_defaults():
    schema = FiltrosAtendimentoSchema()
    resultado = schema.load({})
    
    assert resultado["page"] == 1
    assert resultado["limit"] == 10


def test_filtros_page_e_limit_validos():
    schema = FiltrosAtendimentoSchema()
    resultado = schema.load({"page": "3", "limit": "50"})
    
    assert resultado["page"] == 3
    assert resultado["limit"] == 50

def test_filtros_page_invalido():
    schema = FiltrosAtendimentoSchema()
    
    with pytest.raises(ValidationError) as erro:
        schema.load({"page": "0"})
    
    assert "page" in erro.value.messages

def test_filtros_page_invalido_valor_negativo():
    schema = FiltrosAtendimentoSchema()
    
    with pytest.raises(ValidationError) as erro:
        schema.load({"page": "-1"})
    
    assert "page" in erro.value.messages


def test_filtros_limit_maior_que_100():
    schema = FiltrosAtendimentoSchema()
    
    with pytest.raises(ValidationError) as erro:
        schema.load({"limit": "101"})
    
    assert "limit" in erro.value.messages

def test_filtros_condicao_saude_valida():
    schema = FiltrosAtendimentoSchema()
    resultado = schema.load({"condicao_saude": "hipertensao"})
    
    assert resultado["condicao_saude"] == "hipertensao"

def test_filtros_condicao_saude_valida():
    
    schema = FiltrosAtendimentoSchema()
    
    with pytest.raises(ValidationError) as erro:
        schema.load({"condicao_saude" : "cancer"})
        
    assert "condicao_saude" in erro.value.messages

def test_filtros_data_atendimento_valida():
    dados = {"data_atendimento" : "2023-01-01"}
    
    resultado = FiltrosAtendimentoSchema().dump(dados)
    
    assert resultado["data_atendimento"] == "2023-01-01"


def test_filtros_data_atendimento_invalida():
    dados = {"data_atendimento" : "2023/01/01"}
    
    schema = FiltrosAtendimentoSchema()
    
    with pytest.raises(ValidationError) as erro:
        schema.load(dados)
    
    assert "data_atendimento" in erro.value.messages
    
# Testes do PeriodoAtendimentoSchema

def test_periodo_valido():
    dados = {"data_inicio" : "2023-01-01", "data_fim" : "2023-01-31" }
    
    schema = PeriodoAtendimentoSchema()
    
    resultado = schema.load(dados)
    
    assert resultado["data_inicio"] == "2023-01-01"
    assert resultado["data_fim"] == "2023-01-31"

def test_periodo_invalido():
    dados = {"data_inicio" : "2023/01/01", "data_fim" : "2023/01/31" }
    
    schema = PeriodoAtendimentoSchema()
        
    with pytest.raises(ValidationError) as erro:
        schema.load(dados)
        
    assert "data_inicio" in erro.value.messages  and "data_fim" in erro.value.messages 


def test_periodo_data_inicio_ausente():
    dados = { "data_fim" : "2022-01-01" }

    schema = PeriodoAtendimentoSchema()
    
    with pytest.raises(ValidationError) as erro:
        schema.load(dados)
    
    assert "data_inicio" in erro.value.messages

def test_periodo_data_fim_ausente():
    dados = { "data_inico" : "2022-01-01" }

    schema = PeriodoAtendimentoSchema()
    
    with pytest.raises(ValidationError) as erro:
        schema.load(dados)
    
    assert "data_fim" in erro.value.messages

def test_periodo_data_inicio_maior_que_data_fim():
    dados = {"data_inicio" : "2023-01-01", "data_fim" : "2022-01-01" }
    
    schema = PeriodoAtendimentoSchema()
        
    with pytest.raises(ValidationError) as erro:
        schema.load(dados)
    
    assert "data_inicio" in erro.value.messages 

