# Campus Cultural Backend

API backend do projeto usando Python.

## O que este projeto usa

- `FastAPI`: camada HTTP. Recebe requisições, valida entrada e devolve respostas da API.
- `Pydantic`: validação dos dados de entrada e saída da API.
- `SQLAlchemy`: camada de acesso a dados. Faz a comunicação com o banco SQLite.
- `Alembic`: controle de versões do banco de dados (migrations).
- `Pytest`: testes automatizados.
- `Ruff`: lint e formatação de código.
- `Taskipy`: atalhos para comandos frequentes.
- `SQLite`: banco de dados local em arquivo.

## Arquitetura usada

O projeto segue uma separação simples por camadas:

- `Controller`: recebe a requisição HTTP pelo FastAPI, valida os dados com Pydantic e chama a próxima camada.
- `Service`: concentra a regra de negócio.
- `Repository`: faz o acesso ao banco com SQLAlchemy.

Fluxo geral:

`Request HTTP -> Controller -> Service -> Repository -> Banco de Dados`

## Estrutura de pastas

- `api/features/`: código onde ficarão os recursos.
- `api/shared`: código reutilizável da aplicação.
- `database/config`: configuração do banco e da sessão.
- `tests`: testes automatizados.
- `alembic`: arquivos de migration.

## Como instalar as dependências

Se ainda não instalou as dependências do projeto:

```bash
uv sync
```

## Como iniciar o projeto

Comando para subir a API em modo de desenvolvimento:

```bash
uv run task dev
```

Depois disso, a API ficará disponível em:

- `http://127.0.0.1:8000`
- Documentação automática: `http://127.0.0.1:8000/docs`

## Comandos úteis

Executar os testes:

```bash
uv run task test
```

Verificar problemas no código:

```bash
uv run task lint
```

Formatar o código:

```bash
uv run task format
```

Executar lint + testes:

```bash
uv run task check
```

Aplicar migrations:

```bash
uv run task db-upgrade
```

Criar uma nova migration:

```bash
uv run task db-revision -- "nome_da_migration"
```

## Banco de dados

O projeto usa SQLite. O banco local fica no arquivo:

`/Users/diego/dev/projects/utfpr/campus-cultural/backend/database/app.db`

Se quiser limpar o banco local, use:

```bash
uv run task db-clean
```

Na próxima execução da aplicação, o arquivo será criado novamente.

## Testes

Os testes atuais cobrem o CRUD básico de `Usuario`:

- criar
- listar
- buscar por id
- atualizar
- remover

## Observação

Este projeto foi organizado para ficar simples de entender e fácil de evoluir. A ideia é manter cada responsabilidade em sua própria camada, para o código ficar mais limpo e mais fácil de manter.
