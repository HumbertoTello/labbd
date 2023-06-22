-- Criação da tabela Log_Table
DROP TABLE IF EXISTS Log_Table CASCADE;
CREATE TABLE Log_Table (
    LogId SERIAL PRIMARY KEY,
    UserId INTEGER REFERENCES users(UserId),
    LoginDate DATE,
    LoginTime TIME
);