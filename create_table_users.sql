-- Criação da tabela USERS
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    UserId SERIAL PRIMARY KEY,
    Login TEXT UNIQUE,
    Password TEXT,
    Tipo TEXT CHECK(Tipo IN ('Administrador', 'Escuderia', 'Piloto')),
    IdOriginal INTEGER
);

/* Criação de uma TRIGGER para que sempre que um piloto for criado ou 
modificado, o registro na tabela USERS ser corrigido também */
CREATE OR REPLACE FUNCTION update_user_on_driver_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO users (Login, Password, Tipo, IdOriginal)
    VALUES (NEW.DriverRef || '_d', NEW.DriverRef, 'Piloto', NEW.DriverId);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER driver_insert
AFTER INSERT ON Driver
FOR EACH ROW
EXECUTE PROCEDURE update_user_on_driver_insert();

/* Criação de uma TRIGGER para que sempre que um piloto for criado ou 
modificado, o registro na tabela DRIVER ser corrigido também */
CREATE OR REPLACE FUNCTION update_user_on_constructor_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO users (Login, Password, Tipo, IdOriginal)
    VALUES (NEW.ConstructorRef || '_c', NEW.ConstructorRef, 'Escuderia', NEW.ConstructorId);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER constructor_insert
AFTER INSERT ON Constructors
FOR EACH ROW
EXECUTE PROCEDURE update_user_on_constructor_insert();

-- Cadastro do usuário Admin
INSERT INTO users (Login, Password, Tipo)
VALUES ('admin', md5('admin'), 'Administrador');

-- Cadastro de pilotos
INSERT INTO users (Login, Password, Tipo, IdOriginal)
SELECT DriverRef || '_d', md5(DriverRef), 'Piloto', DriverId
FROM Driver;

-- Cadastro de escuderias
INSERT INTO users (Login, Password, Tipo, IdOriginal)
SELECT ConstructorRef || '_c', md5(ConstructorRef), 'Escuderia', ConstructorId
FROM Constructors;
