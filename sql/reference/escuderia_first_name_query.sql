-- Consulta por Primeiro Nome
SELECT DISTINCT D.Forename || ' ' || D.Surname AS complete_name, D.Dob, D.Nationality
FROM Driver AS D
INNER JOIN Results AS R ON R.DriverId = D.DriverId
INNER JOIN Constructors AS C ON C.ConstructorId = R.ConstructorId
WHERE LOWER(C.Name) = LOWER(<escuderia_name>) AND
      LOWER(D.Forename) = LOWER(<piloto_forename>);
