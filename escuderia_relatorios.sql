
-- Relatório 3: Lista os pilotos da escuderia, bem como a quantidade de vezes em
-- que cada um deles alcançou a primeira posição em uma corrida. Os pilotos são
-- identificados por seu nome completo.

-- indices
-- results (driverid,constructor) insert(position)
-- drivers (driverid) insert name insert(forename,surname)

create or replace function pilotos_por_escuderia_rel_3(
    IN _id int)
    RETURNS TABLE(Nome text,Vitorias int) as $$
BEGIN
    RETURN QUERY
    with drivers_results as(
        SELECT driverid,
               COUNT(driverid) filter ( where position = 1) as Vitorias
        FROM Results
        WHERE ConstructorId = _id
        GROUP BY driverid
    ) select
          d.forename||' '||d.surname::text as Nome,
          dr.Vitorias::int
    from drivers_results dr
             join driver d on dr.driverid=d.driverid
    order by Vitorias desc;
END; $$ language plpgsql;


-- indices
-- results (driverid,constructor) insert(position)
-- drivers (driverid) insert name insert(forename,surname)
drop index if exists idx_results_relatorio3;
create index idx_results_relatorio3 ON
    results(driverid,constructorid) include(position);

explain analyse verbose
select pilotos_por_escuderia_rel_3(1);

-- Relatório 4: Lista a quantidade de resultados por cada status, apresentando o
-- status e sua contagem, limitadas ao escopo de sua escuderia


create or replace function status_por_escuderia_rel_4(
    IN _id int)
    RETURNS TABLE(Status text,Quantidade int) as $$
BEGIN
    RETURN QUERY
        with status_construtor as(
            select
                statusid,
               count(1) as Quantidade
            from results
            where constructorid = _id
            group by statusid
        ) select
              s.status as Status,
              sc.Quantidade::int
        from status_construtor sc
             join status s
                 on s.statusid=sc.statusid
        order by 2 desc;
END; $$ language plpgsql;
select * from status_por_escuderia_rel_4(1);

