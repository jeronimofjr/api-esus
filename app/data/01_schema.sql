CREATE TABLE atendimentos (
    ID INTEGER PRIMARY KEY,
    Nome VARCHAR,
    Nascimento DATE,
    CNS VARCHAR,
    CPF VARCHAR(14),
    UNIDADE VARCHAR,
    data_atendimento DATE,
    condicao_saude VARCHAR
);
