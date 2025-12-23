# Guia Rápido de Setup - Docildos

## Passo a Passo Rápido

### 1. Banco de Dados

**Opção A: Docker Local (Desenvolvimento)**
```bash
docker-compose up -d postgres
```

Aguarde ~10 segundos para o PostgreSQL inicializar.

**Opção B: Supabase (Produção/Gratuito)**
1. Criar conta em https://supabase.com
2. Criar novo projeto
3. Copiar connection string
4. Configurar `DATABASE_URL` no `backend/.env`

### 2. LLM Service (Ollama - Gratuito)

**Opção A: Docker (Recomendado)**
```bash
docker-compose up -d ollama
# Aguardar inicialização (~30 segundos)
docker exec -it docildos_ollama ollama pull llama3:8b
```

**Opção B: Instalação Local**
```bash
# Linux/Mac
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3:8b

# Windows: Baixar de https://ollama.com/download
```

### 3. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Editar .env com DATABASE_URL e outras configurações
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### 4. AI Service (em outro terminal)

```bash
cd ai-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Editar .env com LLM_PROVIDER=ollama e BACKEND_API_URL=http://localhost:8000
```

O AI Service será importado pelo backend automaticamente.

**Nota:** Por padrão, o sistema usa Ollama (gratuito). Para usar OpenAI, configure `LLM_PROVIDER=openai` e `OPENAI_API_KEY` no `.env`.

### 5. Frontend (em outro terminal)

```bash
npm install
npm run dev
```

## Verificação

1. **Ollama**: Verificar se está rodando
   ```bash
   curl http://localhost:11434/api/tags
   # ou
   docker ps | grep ollama
   ```

2. **Backend**: http://localhost:8000/docs
   - Deve mostrar documentação interativa da API
   - Health check: http://localhost:8000/health

3. **Frontend**: http://localhost:8080
   - Interface deve carregar normalmente

4. **Teste o chat**: "Me mostra os pedidos de hoje"
   - Deve responder usando Ollama (sem custos de API)

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

### Ollama não está respondendo
- Verifique se o container está rodando: `docker ps | grep ollama`
- Verifique logs: `docker logs docildos_ollama`
- Verifique se o modelo foi baixado: `docker exec docildos_ollama ollama list`
- Reinicie o serviço: `docker-compose restart ollama`

### Erro "LLM Provider não disponível"
- Verifique se Ollama está rodando (se usar LLM_PROVIDER=ollama)
- Verifique se OPENAI_API_KEY está configurada (se usar LLM_PROVIDER=openai)
- Verifique as configurações no arquivo `.env` do ai-service

