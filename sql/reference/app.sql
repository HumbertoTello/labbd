-- Autenticação de usuário no login
SELECT userid, tipo
FROM users
WHERE login = <username> AND password = md5(<password>);

-- Inserção de registro na tabela Log_Table no login
INSERT INTO log_table (UserId, LoginDate, LoginTime)
VALUES (<user_id>, CURRENT_DATE, CURRENT_TIME);