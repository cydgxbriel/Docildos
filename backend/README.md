# Backend - Docildos API

API FastAPI para gestão de confeitaria.

## Setup

1. Criar ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

3. Configurar variáveis de ambiente:
```bash
cp .env.example .env
# Editar .env com suas configurações
```

4. Iniciar PostgreSQL (via Docker):
```bash
docker-compose up -d postgres
```

5. Rodar migrations:
```bash
alembic upgrade head
```

6. Iniciar servidor:
```bash
uvicorn app.main:app --reload --port 8000
```

## Estrutura

- `app/models/` - Modelos SQLAlchemy
- `app/schemas/` - Schemas Pydantic
- `app/api/` - Endpoints REST
- `app/services/` - Lógica de negócio
- `app/db/` - Configuração do banco

