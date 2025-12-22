# AI Service - LangGraph Orchestrator

Serviço de IA usando LangGraph para orquestração de agentes.

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
# Editar .env com sua OPENAI_API_KEY e BACKEND_API_URL
```

## Estrutura

- `agents/supervisor.py` - Agente supervisor
- `agents/tools/` - Tools especializadas
- `graph.py` - Grafo LangGraph principal

