Backend (Python)
================

Conteúdo:
- `app/`: código da aplicação (APIs, serviços, models)
- `tests/`: testes automatizados
- `requirements.txt`: dependências da aplicação
- `pyproject.toml`: configuração de ferramenta (formatador, lint, etc.)

Comandos úteis
--------------
Crie e ative o ambiente virtual:

```bash
python -m venv .venv
.venv\\Scripts\\activate
```

Instale dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação (exemplo FastAPI):

```bash
uvicorn app.main:app --reload --port 8000
```
