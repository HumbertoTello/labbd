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
DECLARE
    existing_driverref INTEGER;
BEGIN
    IF TG_OP = 'INSERT' THEN
        SELECT COUNT(*) INTO existing_driverref FROM Driver WHERE DriverRef = NEW.DriverRef;
        IF existing_driverref = 0 THEN
            INSERT INTO users (Login, Password, Tipo, IdOriginal)
            VALUES (NEW.DriverRef || '_d', md5(NEW.DriverRef), 'Piloto', NEW.DriverId);
        ELSE
            RAISE EXCEPTION 'A referência do Piloto fornecida já existe. Cadastro cancelado.';
        END IF;
    ELSIF TG_OP = 'UPDATE' THEN
        UPDATE users SET login = NEW.driverref || '_d', password = md5(NEW.driverref) WHERE idoriginal = OLD.driverid;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS driver_insert ON Driver;
CREATE TRIGGER driver_insert
BEFORE INSERT OR UPDATE ON Driver
FOR EACH ROW
EXECUTE PROCEDURE update_user_on_driver_insert();

/* Criação de uma TRIGGER para que sempre que uma escuderia for criada ou 
modificada, o registro na tabela USERS ser corrigido também */
CREATE OR REPLACE FUNCTION update_user_on_constructor_insert()
RETURNS TRIGGER AS $$
DECLARE
    existing_constructorref INTEGER;
BEGIN
    IF TG_OP = 'INSERT' THEN
        SELECT COUNT(*) INTO existing_constructorref FROM Constructors WHERE ConstructorRef = NEW.ConstructorRef;
        IF existing_constructorref = 0 THEN
            INSERT INTO users (Login, Password, Tipo, IdOriginal)
            VALUES (NEW.ConstructorRef || '_c', md5(NEW.ConstructorRef), 'Escuderia', NEW.ConstructorId);
        ELSE
            RAISE EXCEPTION 'A referência da Escuderia fornecida já existe. Cadastro cancelado.';
        END IF;
    ELSIF TG_OP = 'UPDATE' THEN
        UPDATE users SET login = NEW.constructorref || '_c', password = md5(NEW.constructorref) WHERE idoriginal = OLD.constructorref;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS constructor_insert ON Constructors;
CREATE TRIGGER constructor_insert
BEFORE INSERT OR UPDATE ON Constructors
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
