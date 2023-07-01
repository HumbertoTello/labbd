DROP MATERIALIZED VIEW IF EXISTS airport_city_distances;

-- Como a distância depende de duas tabelas diferentes, não seria possível
-- utilizar um index normal. Nesse caso, criamos uma materialized view
-- que já armazena as informações de aeroportos próximos de cidades brasileiras
CREATE MATERIALIZED VIEW airport_city_distances AS
SELECT
    a.id as airport_id,
    c.geonameid as city_id,
    earth_distance(ll_to_earth(a.latitude_deg, a.longitude_deg), ll_to_earth(c.lat, c.long)) / 1000 AS distance
FROM
    airports a
        JOIN
    geocities15k c ON (earth_distance(ll_to_earth(a.latitude_deg, a.longitude_deg), ll_to_earth(c.lat, c.long)) / 1000) < 100
WHERE
        a.iso_country = 'BR'
  AND a.type in ('medium_airport', 'large_airport')
;

-- Dois índices são criados para otimizar os joins na consulta de aeroportos próximos a cidades
CREATE INDEX IF NOT EXISTS idx_airport_city_distance_airport_id ON airport_city_distances (airport_id);
CREATE INDEX IF NOT EXISTS idx_airport_city_distance_city_id ON airport_city_distances (city_id);

