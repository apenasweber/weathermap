# Como rodar a aplicação

#### Requisitos mínimos

- Docker/Docker-compose
- Client mongodb(compass), caso queira acessar o banco manualmente.

Obs.: há também endpoints onde os dados do banco de dados são retornados, nao se fazendo necessario o uso do client.

## Instruções para Clonar e Executar a Aplicação

1.  **Clonar o Repositório**:

    `git clone https://github.com/apenasweber/weathermap.git`
    `cd backend-python-creditcard`

2.  **Renomear o Arquivo de Configuração**:
    - Renomeie o arquivo ".env-example" para ".env".
3.  **Construir e Executar a Aplicação e os Testes**:
    - Utilize o comando `docker-compose up --build` para construir/executar a aplicação.
4.  **Acessar a Documentação da API**:
    - Agora você pode acessar [http://localhost:8000/docs](http://localhost:8000/docs) para testar os endpoints manualmente.
5.  **Login e Autenticação**:
    - Clique no endpoint `/login`.
    - Clique em "Try it out".
    - Insira `username` e `password`, contidos em sua .env, e clique em "Execute".
    - Você receberá um `access_token`: copie-o.
    - No topo da página, no lado direito, clique em "Authorize" e cole o token, em seguida clique em "Authorize".
6.  **Uso dos Endpoints Autenticados**:
    - Agora você pode usar todos os endpoints autenticados (tempo de expiração do token é de 20 minutos).

# Como rodar os testes

Em um terminal, independente de ja estar rodando a aplicação ou não, execute:
`docker-compose up --build test`

# Endpoints da API

### 1. Previsão do Tempo por Cidade ou Coordenadas

- **Método e Caminho**: `GET /forecast`
- **Parâmetros**:
  - `city` (opcional): Nome da cidade para a previsão do tempo.
  - `lat` (opcional): Latitude para a previsão do tempo.
  - `lon` (opcional): Longitude para a previsão do tempo.
- **Descrição**: Retorna a previsão do tempo com base no nome da cidade ou nas coordenadas de latitude e longitude fornecidas.

### 2. Obter Todos os Dados de Previsão do Tempo

- **Método e Caminho**: `GET /all`
- **Descrição**: Recupera todos os dados de previsão do tempo armazenados no banco de dados.

### 3. Obter Dados de Previsão do Tempo por ID

- **Método e Caminho**: `GET /by-id/{document_id}`
- **Parâmetros**:
  - `document_id`: ID do documento a ser recuperado do banco de dados.
- **Descrição**: Busca e retorna os dados de previsão do tempo associados ao ID do documento especificado.

### 4. Deletar Todos os Dados de Previsão do Tempo

- **Método e Caminho**: `DELETE /delete-all`
- **Descrição**: Remove todos os dados de previsão do tempo do banco de dados.

### 5. Deletar Dados de Previsão do Tempo por ID

- **Método e Caminho**: `DELETE /delete-by-id/{document_id}`
- **Parâmetros**:
  - `document_id`: ID do documento a ser removido do banco de dados.
- **Descrição**: Remove um documento de previsão do tempo específico, identificado pelo ID fornecido.

### 6. Login

- **Método e Caminho**: `POST /login`
- **Parâmetros**:
  - `username`: Nome de usuário para login.
  - `password`: Senha para login.
- **Descrição**: Endpoint para realizar o login. Retorna um token JWT se o login for bem-sucedido.

# Benefícios Clean Arch

- **Separação de Responsabilidades**: Cada parte da aplicação tem um trabalho específico, tornando o código mais fácil de entender, manter e desenvolver.
- **Testabilidade**: Com seções separadas para diferentes aspectos do aplicativo, fica mais fácil testar unidades individuais de código.
- **Escalabilidade**: Com Docker e código modular, é mais fácil escalar a aplicação conforme necessário.
- **Organização**: O código é mais fácil de encontrar em um projeto bem estruturado.
- **Controle de Versão**: A separação também ajuda no gerenciamento de controle de versão, pois as mudanças podem ser isoladas em áreas específicas do projeto.
- **Gestão de Migração de Banco de Dados**: Com Alembic, as mudanças no esquema do banco de dados são rastreadas e gerenciadas de forma eficaz. Isso simplifica a evolução do esquema e o controle de versão.
- **Reutilização**: Com uma estrutura bem definida, fica mais fácil reutilizar componentes conforme necessário.
- **Segurança**: Armazenar dados sensíveis em variáveis de ambiente (arquivo .env) protege as informações de serem expostas.

## Estrutura da Aplicação

- **app**: É onde reside a lógica principal do aplicativo. Está dividido em vários subdiretórios:
  - **api**: Contém a versão da API e seus endpoints. No meu caso, a versão v1 da API.
  - **auth**: É onde a lógica de autenticação é tratada. Tenho diferentes módulos para diferentes funcionalidades de autenticação.
  - **endpoints**: Contém os diferentes endpoints da API.
  - **core**: Este diretório mantém a funcionalidade central do meu projeto, como conexões com o banco de dados e configurações.
- **models**: Inclui os modelos de banco de dados. São representações pythonicas das tabelas do banco de dados.
- **schemas**: Contém modelos Pydantic. Os modelos Pydantic permitem a análise, validação e serialização de dados (convertendo-os em JSON).
- **tests**: Este diretório contém todos os meus casos de teste, divididos em testes unitários, de integração e de estresse.
- **.env e .env-example**: Esses arquivos são usados para armazenar variáveis de ambiente.
- **docker-compose.yaml e Dockerfile**: Esses arquivos são usados para contêinerizar a aplicação e gerenciar serviços, fornecendo um ambiente isolado para a execução do aplicativo.
- **requirements.txt**: Este arquivo lista todas as dependências da biblioteca Python que precisam ser instaladas usando pip install.

---

Esta estrutura oferece uma visão organizada e detalhada dos componentes principais do seu aplicativo, destacando as funções de cada diretório e arquivo.
