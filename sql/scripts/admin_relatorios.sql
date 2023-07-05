CREATE OR REPLACE FUNCTION status_results()
RETURNS REFCURSOR
AS $$
DECLARE 
    l_cursor REFCURSOR;
BEGIN
    OPEN l_cursor FOR
        SELECT s.status, COUNT(*)
        FROM results r
                 JOIN status s ON s.statusid = r.statusid
        GROUP BY s.status
        ORDER BY s.status;

    RETURN l_cursor;
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_airport_data(p_city_name TEXT)
RETURNS REFCURSOR
AS $$
DECLARE 
    l_cursor REFCURSOR;
BEGIN
    OPEN l_cursor FOR
        SELECT c.name, a.iatacode, a.name, a.city,
               ROUND(CAST(d.distance AS NUMERIC(10, 2)), 2) AS distance,
               CASE
                   WHEN type = 'medium_airport' THEN 'Aeroporto médio'
                   WHEN type = 'large_airport' THEN 'Aeroporto grande'
                   ELSE type
                   END AS formatted_column
        FROM airports a
                 JOIN airport_city_distances d ON a.ident = d.airport_id
                 JOIN geocities15k c ON c.geonameid = d.city_id
        WHERE type IN ('medium_airport', 'large_airport')
            AND isocountry = 'BR'
            AND lower(c.name) = lower(p_city_name)
        ORDER BY distance;
    
    RETURN l_cursor;
END; $$ LANGUAGE plpgsql;