# Guia Rápido de Setup - Docildos

## Passo a Passo Rápido

### 1. Banco de Dados
```bash
docker-compose up -d postgres
```

Aguarde ~10 segundos para o PostgreSQL inicializar.

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Editar .env com OPENAI_API_KEY
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### 3. AI Service (em outro terminal)

```bash
cd ai-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Editar .env com OPENAI_API_KEY e BACKEND_API_URL=http://localhost:8000
```

O AI Service será importado pelo backend automaticamente.

### 4. Frontend (em outro terminal)

```bash
npm install
npm run dev
```

## Verificação

1. Backend rodando: http://localhost:8000/docs
2. Frontend rodando: http://localhost:8080
3. Teste o chat com: "Me mostra os pedidos de hoje"

## Problemas Comuns

### Erro de conexão com banco
- Verifique se o Docker está rodando: `docker ps`
- Verifique se o PostgreSQL está ativo: `docker-compose ps`

### Erro de importação no backend
- Certifique-se de que o `ai-service` está no mesmo nível que `backend`
- Verifique se as dependências do ai-service estão instaladas

### Erro de CORS
- Verifique se o frontend está usando a porta correta (8080 ou 5173)
- Adicione a porta no CORS do backend se necessário

### Reconhecimento de voz não funciona
- Use Chrome ou Edge (suporte melhor para Web Speech API)
- Verifique permissões do microfone no navegador

