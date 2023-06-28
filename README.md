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

    > Observe que o link do Google Drive fornecido neste projeto é acessível apenas para usuários da Universidade de São Paulo (USP). Certifique-se de estar logado com um e-mail que termine com @usp.br para obter acesso ao conteúdo do Google Drive.

3. **Execute os .sql**

    1. Utilize a query contida no arquivo `create_table_users.sql` para criar a tabela `users` no seu banco de dados local.

    2. Utilize a query contida no arquivo `create_table_log_table.sql` para criar a tabela `log_table` no seu banco de dados local.

    3. Utilize a query contida no arquivo `extensions.sql` para instalar as extensões necessárias no seu banco de dados local.

    4. Utilize a query contida no arquivo `create_index_airport.sql` para criar o índice usado no Relatório 2 de Admin.

## Execução

Após a configuração inicial, você pode executar o projeto com o seguinte comando:

```sh
python app.py
```

## Acesso à Aplicação

O acesso à ferramenta só pode ser feito por meio de login, onde cada usuário terá acesso específico com base no seu tipo de usuário.

### Usuário Administrador

- Login: admin
- Senha: admin
- Descrição: O usuário administrador tem acesso completo a todas as informações da base de dados. Ele pode visualizar, editar e gerenciar todas as informações disponíveis na aplicação.

### Usuário Escuderia

- Login: [constructorref]_c
- Senha: [constructorref]
- Exemplo: Para a escuderia McLaren:
  - Login: mclaren_c
  - Senha: mclaren
- Descrição: O usuário escuderia tem acesso somente às informações relacionadas à sua escuderia específica e aos pilotos que correm por ela. Ele pode visualizar e editar apenas essas informações específicas.

### Usuário Piloto

- Login: [driverref]_d
- Senha: [driverref]
- Exemplo: Para o piloto Hamilton:
  - Login: hamilton_d
  - Senha: hamilton
- Descrição: O usuário piloto tem acesso às informações relacionadas ao seu próprio desempenho. Ele pode visualizar e editar informações específicas sobre suas corridas, pontuações e estatísticas individuais.
