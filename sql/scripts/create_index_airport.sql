DROP MATERIALIZED VIEW IF EXISTS airport_city_distances;

-- Como a distância depende de duas tabelas diferentes, não seria possível
-- utilizar um index normal. Nesse caso, criamos uma materialized view
-- que já armazena as informações de aeroportos próximos de cidades brasileiras
CREATE MATERIALIZED VIEW airport_city_distances AS
SELECT
    a.ident as airport_id,
    c.geonameid as city_id,
    earth_distance(ll_to_earth(a.latdeg, a.longdeg), ll_to_earth(c.lat, c.long)) / 1000 AS distance
FROM
    airports a
        JOIN
    geocities15k c ON (earth_distance(
        ll_to_earth(a.latdeg, a.longdeg),
        ll_to_earth(c.lat, c.long)) / 1000) < 100 -- distancia retornada pela função é em metros
WHERE
        a.isocountry = 'BR'
  AND a.type in ('medium_airport', 'large_airport')
;

-- Não foi possível otimizar refresh da materialized view,
-- contudo os índices abaixo otimizam geocities, que não possuía primary key
-- e indexa city_id para a materialized view que por padrão não tem índices
drop index if exists idx_airport_city_distance_city_id;
drop index if exists pkgeocities15k; -- antes `Rio de Janeiro`: 6.3ms -> 0.25ms
CREATE INDEX IF NOT EXISTS idx_airport_city_distance_city_id ON airport_city_distances (city_id);
CREATE INDEX IF NOT EXISTS pkgeocities15k ON geocities15k(name);

-- função de refresh da materialized view de distâncias de aeroporto e cidade
CREATE OR REPLACE FUNCTION refresh_airport_city_distance()
    returns trigger
    language plpgsql as
$$ begin
    refresh materialized view airport_city_distances;
    return null;
end $$;


-- triggers do refresh para recaulcular distâncias se tabelas de cidade ou aeroporto atualizarem
-- ou receberem novas tuplas. Atualização feita após inserção e por statement
DROP TRIGGER IF EXISTS airport_insert ON airports;
CREATE TRIGGER airport_insert
AFTER INSERT OR UPDATE OR DELETE
    ON airports
FOR EACH STATEMENT
EXECUTE PROCEDURE update_user_on_driver_insert();

DROP TRIGGER IF EXISTS cities_insert ON geocities15k;
CREATE TRIGGER cities_insert
    AFTER INSERT OR UPDATE OR DELETE
    ON geocities15k
    FOR EACH STATEMENT
EXECUTE PROCEDURE update_user_on_driver_insert();
