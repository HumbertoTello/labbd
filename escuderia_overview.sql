-- funções de overview da escuderia

-- quantidade de vitórias da escuderia;
create or replace function quant_vitorias_escuderia(_id INT)
    RETURNS INT as $$
    DECLARE _result INT;
BEGIN
    SELECT COUNT(*)::int  INTO _result
    FROM Results
    WHERE ConstructorId = _id and
            Position = 1;
    RETURN _result;
END;
$$ language plpgsql;
-- SELECT ConstructorId FROM Constructors WHERE Name = 'McLaren';
-- select quant_vitorias_escuderia(1);

-- quantidade de pilotos diferentes que já correram pela escuderia
create or replace function quant_pilotos_diferentes(_id INT)
    RETURNS INT as $$
DECLARE _result INT;
BEGIN
    SELECT count(distinct(driverid)) into _result
    FROM Results
    WHERE ConstructorId =_id;
    RETURN _result;
END;
$$ language plpgsql;
-- select quant_pilotos_diferentes(1);


-- Consulta para obter o primeiro ano em que há dados da escuderia na base
create or replace function primeiro_ultimo_ano_escuderia(
    IN _id int,
    OUT _min date,
    OUT _max date) as $$
BEGIN
    SELECT min(date) INTO _min
    FROM Results re
             join races ra on re.raceid = ra.raceid
    WHERE ConstructorId =_id;
    SELECT max(date) INTO _max
    FROM Results re
             join races ra on re.raceid = ra.raceid
    WHERE ConstructorId =_id;
END; $$ language plpgsql;
-- select primeiro_ultimo_ano_escuderia(1);

