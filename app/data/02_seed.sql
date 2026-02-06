COPY atendimentos
FROM '/docker-entrypoint-initdb.d/atendimentos.csv'
DELIMITER ','
CSV HEADER;

