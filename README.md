# Projeto de Laboratório de Base de Dados

## Descrição do Projeto

Este projeto é uma ferramenta interativa de acesso à uma base de dados da Fórmula 1, permitindo que usuários autenticados (admin, escuderias e pilotos) visualizem e interajam com os dados de maneira personalizada. A interface é dividida em três telas principais (login, overview e relatórios), cada uma proporcionando diferentes funcionalidades e níveis de interação com os dados.

## Configuração Inicial

Para configurar o projeto localmente, siga os passos abaixo:

1. **Instale as dependências do projeto**

    Este projeto utiliza a biblioteca `psycopg2` para conexão com o PostgreSQL. Você pode instalar a biblioteca utilizando o comando abaixo:

    ```sh
    pip install psycopg2
    ```

    > Nota: Este projeto assume que você está utilizando Python 3. Certifique-se de que o comando `pip` está vinculado ao Python 3. Se não estiver, você pode precisar usar `pip3` ao invés de `pip`.

2. **Configure a conexão com o banco de dados**

    Crie um arquivo `config.ini` baseado no arquivo de exemplo `config.ini.example` para configurar a conexão com o seu banco de dados PostgreSQL local. O banco de dados deve conter os dados da Fórmula 1.

    Os arquivos originais para a carga de dados podem ser encontrados no Google Drive, disponíveis [aqui](https://drive.google.com/drive/folders/13TQKEhQbwXMtd1MJ_oYFplgu8ets4QsO?usp=sharing).

3. **Crie a tabela `users` e `log_table`**

    1. Utilize a query contida no arquivo `create_table_users.sql` para criar a tabela `users` no seu banco de dados local.

    2. Utilize a query contida no arquivo `create_table_log_table` para criar a tabela `log_table` no seu banco de dados local.

## Execução

Após a configuração inicial, você pode executar o projeto com o seguinte comando:

```sh
python main.py
```
