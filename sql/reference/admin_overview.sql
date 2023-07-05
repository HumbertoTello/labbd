-- Como as queries usadas no overview do admin são muito simples,
-- decidimos não implementá-las como funções separadas. Ao invés
-- disso, elas estão hardcoded. A saber, elas são as sequintes:

SELECT COUNT(*) FROM driver; -- para piloto
SELECT COUNT(*) FROM constructors; -- para escuderia
SELECT COUNT(*) FROM races; -- para corridas
SELECT COUNT(*) FROM seasons; -- para temporadas