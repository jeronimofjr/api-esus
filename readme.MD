# API REST para Acesso a Dados de Saúde

Este projeto consiste no desenvolvimento de uma API REST para acesso estruturado a dados de atendimentos de saúde, originalmente exportados de um sistema de terceiros em formato CSV. O objetivo é disponibilizar esses dados de forma segura, padronizada e eficiente para consumo por equipes de Ciência de Dados e outros sistemas corporativos.

A API foi desenvolvida em Python utilizando o framework Flask, seguindo boas práticas de arquitetura, validação de dados, testes automatizados e documentação.

# Orientações

O banco de dados é representado pelo arquivo `atendimentos.csv`

# Implementação da API

A API expõe endpoints REST para consulta de atendimentos de saúde, suportando paginação de resultados, filtros por período e unidade, validação rigorosa de entradas e respostas padronizadas. A aplicação foi estruturada em camadas bem definidas, com foco em manutenibilidade, testabilidade e clareza do fluxo de dados.

## Tecnologias

| Tecnologia        | Versão   | Descrição                                                                                                                            |
| ----------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Python            | `3.1.0`  | Linguagem utilizada para implementar a lógica de negócio e regras de domínio da aplicação.                                           |
| Flask             | `3.1.2`  | Framework web para desenvolvimento de API REST corporativa, com foco em simplicidade e controle do fluxo de requisições.             |
| SQLAlchemy        | `2.0.46` | ORM utilizado para mapeamento objeto-relacional, abstração do acesso a dados e maior controle sobre persistência e transações.       |
| Marshmallow       | `9.0.2`  | Validação, serialização e sanitização de dados sensíveis, contribuindo para a integridade das informações e conformidade com a LGPD. |
| Pytest            | `9.0.2`  | Testes automatizados para garantir confiabilidade, consistência e segurança da API.                                                  |
| Docker            | `26.1.0` | Containerização da aplicação, assegurando isolamento, reprodutibilidade e padronização do ambiente.                                  |
| Docker Compose    |          | Orquestração dos serviços da aplicação, facilitando o setup e execução em ambientes corporativos.                                    |
| OpenAPI (Swagger) |          | Documentação padronizada da API, permitindo transparência dos contratos e facilitando auditorias e integrações.                      |

## Pré-requisitos

- Docker >= 26.1.0
- Docker Compose >= 2.0
- 2GB RAM disponível
- Porta **8001** livre

## Arquitetura

O projeto utiliza arquitetura em camadas, promovendo separação de responsabilidades, facilidade de manutenção e testes:

- **Controllers:** camada HTTP, responsável por receber requisições, aplicar validações e retornar respostas padronizadas
- **Services:** regras de negócio e orquestração dos fluxos da aplicação
- **Repositories:** acesso e abstração da camada de dados
- **Schemas:** validação, serialização e desserialização de dados de entrada e saída
- **Models:** representação das entidades de domínio

## Funcionalidades

- Consulta paginada de atendimentos de saúde, evitando sobrecarga e facilitando o consumo de grandes volumes de dados
- Filtros por período e unidade de atendimento
- Validação e sanitização de dados de entrada e saída utilizando schemas dedicados
- Respostas padronizadas em toda a API, garantindo consistência e previsibilidade para consumidores
- Tratamento centralizado de erros por meio de handlers globais
- Documentação interativa da API utilizando OpenAPI (Swagger)
- Testes automatizados cobrindo rotas e schemas, assegurando confiabilidade e estabilidade da aplicação

## Estrutura

```bash
.
├── app
│   ├── config
│   │   ├── database.py
│   │   └── __init__.py
│   ├── controllers
│   │   ├── atendimento_controller.py
│   │   ├── __init__.py
│   │   └── system_controller.py
│   ├── data
│   │   ├── 01_schema.sql
│   │   ├── 02_seed.sql
│   │   ├── atendimentos.csv
│   │   └── __init__.py
│   ├── Dockerfile
│   ├── __init__.py
│   ├── models
│   │   ├── atendimentos.py
│   │   └── __init__.py
│   ├── repositories
│   │   ├── atendimento_repository.py
│   │   └── __init__.py
│   ├── requirements.txt
│   ├── run.py
│   ├── schemas
│   │   ├── atendimento_schema.py
│   │   └── __init__.py
│   ├── services
│   │   ├── atendimento_service.py
│   │   └── __init__.py
│   ├── tests
│   │   ├── conftest.py
│   │   ├── __init__.py
│   │   ├── test_rotas.py
│   │   └── test_schemas.py
│   └── utils
│       ├── error_handlers.py
│       ├── __init__.py
│       ├── responses.py
│       └── swagger.py
├── docker-compose.yml
└── docs
    └── openapi.yml
```

## Instruções de uso

Clone o repositório do projeto:

```bash
git clone <url>
```

Acesse o diretório do projeto

```bash
cd <nome-do-diretorio>
```

Na raiz do projeto crie um arquivo `.env` e o preecha de acordo com o exemplo dado no arquivo `.env.example`

Suba a aplicação utilizando Docker Compose:

```bash
docker compose up --build
```

Após a inicialização dos containers, a API estará disponível para consumo.

---

### Acesso à API e Documentação

- **URL Base:** `http://127.0.0.1:8001/api/v1/`

A documentação interativa da API pode ser acessada via Swagger:

- **Swagger UI:** `http://127.0.0.1:8001/api/v1/docs`

### Principais Endpoints

| Método | Rota                                           | Descrição                                                        |
| ------ | ---------------------------------------------- | ---------------------------------------------------------------- |
| GET    | `/atendimentos`                                | Lista atendimentos com paginação                                 |
| GET    | `/atendimentos/periodo?data_inicio=&data_fim=` | Consulta atendimentos por período                                |
| GET    | `/atendimentos/{id}`                           | Filtra atendimentos por id                                       |
| GET    | `/atendimentos/stats`                          | Lista estatísticas dos Atendimentos                              |
| GET    | `/info`                                        | Lista informações da API, endpoints, docs, nome, status e versão |
| GET    | `/health-check`                                | Status da API                                                    |

### Exemplo de uso

**Listagem simples com paginação**

```http
curl http://127.0.0.1:8001/api/v1/atendimentos?limit=3
```

**Quando usar**
Para consumir dados paginados ou popular listagens no front-end.

**Saída:**

```json
{
  "data": {
    "atendimentos": [
      {
        "cns": "75983412655",
        "condicao_saude": "hipertensao",
        "cpf": "***.***.***-87",
        "data_atendimento": "2023-08-10",
        "id": 0,
        "nascimento": "1978-04-05",
        "nome": "Elisa Pinto",
        "unidade": "Unidade de saude Maria Alice"
      },
      {
        "cns": "75983412655",
        "condicao_saude": "diabetes",
        "cpf": "***.***.***-87",
        "data_atendimento": "2023-12-19",
        "id": 1,
        "nascimento": "1978-04-05",
        "nome": "Elisa Pinto",
        "unidade": "Unidade de saude Maria Alice"
      },
      {
        "cns": "75983412655",
        "condicao_saude": "diabetes",
        "cpf": "***.***.***-87",
        "data_atendimento": "2023-11-06",
        "id": 2,
        "nascimento": "1978-04-05",
        "nome": "Elisa Pinto",
        "unidade": "Unidade de saude Maria Alice"
      }
    ]
  },
  "pagination": {
    "limit": 3,
    "page": 1,
    "total_pages": 3111
  },
  "success": true,
  "total_items": 9331
}
```

**Consulta por período**

```http
curl http://127.0.0.1:8001/api/v1/atendimentos/periodo?data_inicio=2024-01-01&data_fim=2024-01-02
```

**Quando usar:**
Para análises temporais ou geração de relatórios.

**Estatísticas agregadas**

```http
curl http://127.0.0.1:8001/api/v1/atendimentos/stats
```

**Quando usar:**
Para dashboards, indicadores e métricas de saúde.

**Saída:**

```json
{
  "data": {
    "atendimentos_por_condicao_saude": {
      "dengue": 2353,
      "diabetes": 2342,
      "ferida vascular": 2319,
      "hipertensao": 2317
    },
    "total_atendimentos": 9331,
    "total_pessoas_unicas": 934
  },
  "success": true
}
```

**Mesclando filtros**

```http
http://127.0.0.1:8001/api/v1/atendimentos?condicao_saude=diabetes&unidade=Unidade%20de%20saude%20Maria%20Alice&limit=3
```

**Quando usar:**
Para consultas refinadas e cruzamento de dados.
