from unittest.mock import patch

@patch("app.controllers.atendimento_controller.AtendimentoService")
def test_listar_atendimentos(mock_service, client):
    
    mock_service.return_value.get_all_atendimentos.return_value = (
        [
            {"id": 1, "nome": "João"},
            {"id": 2, "nome": "Maria"}
        ],
        2  
    )
    
    response = client.get("/api/v1/atendimentos")
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["success"] is True
    assert data["total_items"] == 2
    assert len(data["data"]["atendimentos"]) == 2


@patch("app.controllers.atendimento_controller.AtendimentoService")
def test_listar_atendimentos_vazio(mock_service, client):
    mock_service.return_value.get_all_atendimentos.return_value = ([], 0)
    
    response = client.get("/api/v1/atendimentos")
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["success"] is True
    assert data["total_items"] == 0
    assert data["data"]["atendimentos"] == []

@patch("app.controllers.atendimento_controller.AtendimentoService")
def test_listar_atendimentos_com_paginacao(mock_service, client):
    mock_service.return_value.get_all_atendimentos.return_value = (
        [{"id": 1}],
        25
    )
    
    response = client.get("/api/v1/atendimentos?page=2&limit=5")
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["pagination"]["page"] == 2
    assert data["pagination"]["limit"] == 5
    assert data["pagination"]["total_pages"] == 5

@patch("app.controllers.atendimento_controller.AtendimentoService")
def test_listar_atendimentos_com_filtro_unidade(mock_service, client):
    mock_service.return_value.get_atendimentos_by_filters.return_value = (
        [{"id": 1, "unidade": "UBS Central"}],
        1
    )
    
    response = client.get("/api/v1/atendimentos?unidade=UBS+Central")
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["total_items"] == 1

def test_listar_atendimentos_condicao_invalida(client):
    response = client.get("/api/v1/atendimentos?condicao_saude=invalida")
    data = response.get_json()
    
    assert response.status_code == 400
    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_listar_atendimentos_page_invalido(client):
    response = client.get("/api/v1/atendimentos?page=0")
    data = response.get_json()
    
    assert response.status_code == 400
    assert "page" in data["error"]["details"]

@patch("app.controllers.atendimento_controller.AtendimentoService")
def test_buscar_atendimento_por_id(mock_service, client):
    mock_service.return_value.get_atendimento_by_id.return_value = {
        "id": 1,
        "nome": "João"
    }
    
    response = client.get("/api/v1/atendimentos/1")
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["success"] is True
    assert data["data"]["atendimento"]["id"] == 1


@patch("app.controllers.atendimento_controller.AtendimentoService")
def test_buscar_atendimento_nao_encontrado(mock_service, client):
    mock_service.return_value.get_atendimento_by_id.return_value = None
    
    response = client.get("/api/v1/atendimentos/9999")
    data = response.get_json()
    
    assert response.status_code == 404
    assert data["success"] is False
    assert data["error"] == "Atendimento not found"

@patch("app.controllers.atendimento_controller.AtendimentoService")
def test_buscar_por_periodo(mock_service, client):
    mock_service.return_value.get_atendimentos_by_period.return_value = [
        {"id": 1, "data_atendimento": "2023-08-10"},
        {"id": 2, "data_atendimento": "2023-08-15"}
    ]
    
    response = client.get(
        "/api/v1/atendimentos/periodo"
        "?data_inicio=2023-08-01&data_fim=2023-08-31"
    )
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["success"] is True
    assert data["total_items"] == 2


@patch("app.controllers.atendimento_controller.AtendimentoService")
def test_buscar_por_periodo_vazio(mock_service, client):
    mock_service.return_value.get_atendimentos_by_period.return_value = []
    
    response = client.get(
        "/api/v1/atendimentos/periodo"
        "?data_inicio=2020-01-01&data_fim=2020-01-02"
    )
    data = response.get_json()
    
    assert response.status_code == 404
    assert data["data"]["atendimentos"] == []


def test_buscar_por_periodo_sem_data_inicio(client):
    response = client.get("/api/v1/atendimentos/periodo?data_fim=2023-08-31")
    data = response.get_json()
    
    assert response.status_code == 400
    assert "data_inicio" in data["error"]["details"]


def test_buscar_por_periodo_sem_data_fim(client):
    response = client.get("/api/v1/atendimentos/periodo?data_inicio=2023-08-01")
    data = response.get_json()
    
    assert response.status_code == 400
    assert "data_fim" in data["error"]["details"]


def test_buscar_por_periodo_data_inicio_maior(client):
    response = client.get(
        "/api/v1/atendimentos/periodo"
        "?data_inicio=2023-08-31&data_fim=2023-08-01"
    )
    data = response.get_json()
    
    assert response.status_code == 400
    assert "data_inicio" in data["error"]["details"]
