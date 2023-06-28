-- Quantidade de vitórias do piloto
create or replace function quant_vitorias_piloto(
    IN _id int,
    OUT _res int) as $$
BEGIN
    SELECT COUNT(*)::int INTO _res
    FROM Results
    WHERE driverid=_id and
            Position = 1;
END; $$ language plpgsql;
-- select quant_vitorias_piloto(1);

-- – Primeiro e último ano em que há dados
-- do piloto na base (pela tabela RESULTS).
create or replace function primeiro_ultimo_ano_piloto(
    IN _id int,
    OUT _min date,
    OUT _max date) as $$
BEGIN
    SELECT min(date) INTO _min
    FROM Results re
             join races ra on re.raceid = ra.raceid
    WHERE driverid=_id;
    SELECT max(date) INTO _max
    FROM Results re
             join races ra on re.raceid = ra.raceid
    WHERE driverid=_id;
END; $$ language plpgsql;
-- select primeiro_ultimo_ano_piloto(1);