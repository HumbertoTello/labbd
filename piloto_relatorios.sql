-- Relatório 5: Consultar a quantidade de vitórias obtidas, apresentando o ano e a
-- corrida onde cada vitória foi alcançada.
-- Esse relatório deverá utilizar o comando ROLLUP para permitir a visualização de
-- vitórias por ano e corrida. Portanto, deve aparecer na tabela as sumarizações por
-- ano, por ano e corrida e uma sumarização geral.

-- indexação: results
create or replace function vitorias_piloto_relatorio5(
    IN _id int)
    RETURNS TABLE(Ano int,NomeCorrida text,Quantidade int) as $$
BEGIN
    RETURN QUERY
        select
            ra.year::int as Ano,
            ra.name::text as NomeCorrida,
            count(*)::int as Quantidade
        from results re
                 join races ra on
                re.raceid = ra.raceid
        where re.driverid = _id and
                re.position = 1
        group by rollup(ra.year,ra.name);
END; $$ language plpgsql;
select * from vitorias_piloto_relatorio5(1);


-- Relatório 6: lista a quantidade de resultados por cada status, apresentando o status
-- e sua contagem, limitada ao escopo do piloto logado.