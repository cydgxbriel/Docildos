# Guia de Otimização de Custos - Docildos

Este guia explica como configurar o Docildos para operar com custos mínimos usando serviços open source e gratuitos.

## Visão Geral

O Docildos foi projetado para reduzir custos mensais de operação através de:

1. **LLM Local Gratuito** (Ollama) - Elimina custos de API OpenAI
2. **Hosting Gratuito** - Railway, Render, Vercel (free tiers)
3. **Banco de Dados Gratuito** - Supabase, Neon, Railway PostgreSQL

## Economia Estimada

### Antes (Custos Mensais)
- OpenAI API: $20-100+ (dependendo do uso)
- Hosting Backend: $10-25/mês
- Banco de Dados: $5-15/mês
- **Total: $35-140+/mês**

### Depois (Custos Mensais)
- Ollama (local): $0
- Hosting (free tier): $0-5/mês
- Banco (free tier): $0
- **Total: $0-5/mês**

### Economia: $35-135+/mês (95-100% de redução)

## Configuração de LLM Local (Ollama)

### Passo 1: Instalar Ollama

**Linux/Mac:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Baixe o instalador em: https://ollama.com/download

**Docker:**
```bash
docker-compose up -d ollama
```

### Passo 2: Baixar um Modelo

Modelos recomendados (do menor ao maior):

- **phi3** (3.8B) - Mais rápido, menor qualidade
- **llama3:8b** (8B) - Bom equilíbrio (recomendado)
- **mistral** (7B) - Boa qualidade
- **llama3:70b** (70B) - Melhor qualidade, requer GPU

```bash
# Baixar modelo recomendado
ollama pull llama3:8b

# Ou usar via Docker
docker exec -it docildos_ollama ollama pull llama3:8b
```

### Passo 3: Configurar AI Service

Edite `ai-service/.env`:

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:8b
```

### Passo 4: Testar

```bash
cd ai-service
python -c "from providers.factory import get_llm_provider; p = get_llm_provider(); print('✅ Ollama configurado!')"
```

## Configuração de Banco de Dados Gratuito

### Opção 1: Supabase (Recomendado)

1. Criar conta em https://supabase.com
2. Criar novo projeto
3. Copiar connection string do projeto
4. Editar `backend/.env`:

```env
DATABASE_URL=postgresql://postgres:[SUA_SENHA]@db.[PROJECT_ID].supabase.co:5432/postgres
```

5. Rodar migrações:
```bash
cd backend
alembic upgrade head
```

**Limites Free Tier:**
- 500MB de armazenamento
- 2GB de bandwidth/mês
- Backup automático

### Opção 2: Railway PostgreSQL

1. Criar conta em https://railway.app
2. Criar novo projeto
3. Adicionar serviço PostgreSQL
4. Copiar DATABASE_URL das variáveis de ambiente
5. Configurar no `backend/.env`

**Limites Free Tier:**
- $5 crédito/mês (suficiente para projetos pequenos)
- PostgreSQL incluído

### Opção 3: Neon (Serverless)

1. Criar conta em https://neon.tech
2. Criar projeto
3. Copiar connection string
4. Configurar no `backend/.env`

**Limites Free Tier:**
- 0.5GB de armazenamento
- Auto-scaling
- Backup automático

## Configuração de Hosting Gratuito

### Frontend: Vercel (Recomendado)

1. Criar conta em https://vercel.com
2. Conectar repositório GitHub
3. Configurar build:
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Adicionar variável de ambiente:
   - `VITE_API_URL=https://seu-backend.railway.app`
5. Deploy automático a cada push

**Limites Free Tier:**
- 100GB bandwidth/mês
- Deploy ilimitado
- SSL automático

### Backend: Railway (Recomendado)

1. Criar conta em https://railway.app
2. Criar novo projeto
3. Conectar repositório GitHub
4. Adicionar serviço:
   - Selecione o diretório `backend`
   - Railway detecta automaticamente Python
5. Configurar variáveis de ambiente:
   - `DATABASE_URL` (do Supabase ou Railway PostgreSQL)
   - `CORS_ORIGINS` (URL do frontend)
6. Deploy automático

**Limites Free Tier:**
- $5 crédito/mês
- Sleep após inatividade (pode ser lento no primeiro acesso)

**Solução para Sleep:**
- Usar UptimeRobot (gratuito) para fazer ping a cada 5 minutos
- Ou considerar upgrade mínimo ($5/mês)

### Alternativa: Render

1. Criar conta em https://render.com
2. Criar novo Web Service
3. Conectar repositório
4. Configurar:
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Adicionar variáveis de ambiente

**Limites Free Tier:**
- 750h/mês
- Sleep após 15min inatividade

## Comparação: Ollama vs OpenAI

### Ollama (Gratuito)

**Vantagens:**
- ✅ Zero custo
- ✅ Privacidade total (dados não saem do servidor)
- ✅ Sem rate limits
- ✅ Controle total sobre o modelo

**Desvantagens:**
- ⚠️ Requer servidor com recursos (CPU/GPU)
- ⚠️ Modelos podem ser menos capazes que GPT-4
- ⚠️ Consome recursos do servidor

**Recomendação:**
- Use modelos menores para desenvolvimento (phi3, llama3:8b)
- Modelos maiores para produção se tiver GPU (llama3:70b, mistral)

### OpenAI (Pago)

**Vantagens:**
- ✅ Melhor qualidade (GPT-4)
- ✅ Não consome recursos do servidor
- ✅ Sempre atualizado

**Desvantagens:**
- ❌ Custos por uso ($20-100+/mês)
- ❌ Rate limits
- ❌ Dados enviados para terceiros

**Recomendação:**
- Use apenas como fallback ou para tarefas críticas
- Configure como opcional no `.env`

## Configuração Híbrida (Recomendada)

Você pode usar Ollama para tarefas simples e OpenAI para tarefas críticas:

```python
# Exemplo de lógica híbrida
if task_complexity == "simple":
    use_ollama()
else:
    use_openai()
```

## Monitoramento de Custos

### Verificar Uso de Recursos

**Railway:**
- Dashboard mostra uso de créditos em tempo real
- Alertas quando próximo do limite

**Supabase:**
- Dashboard mostra uso de armazenamento e bandwidth
- Alertas configuráveis

### Scripts Úteis

```bash
# Verificar status do Ollama
curl http://localhost:11434/api/tags

# Ver modelos disponíveis
ollama list

# Testar modelo
ollama run llama3:8b "Olá, como você está?"
```

## Troubleshooting

### Ollama não responde

1. Verificar se está rodando:
   ```bash
   docker ps | grep ollama
   # ou
   curl http://localhost:11434/api/tags
   ```

2. Verificar logs:
   ```bash
   docker logs docildos_ollama
   ```

3. Reiniciar serviço:
   ```bash
   docker-compose restart ollama
   ```

### Banco de Dados não conecta

1. Verificar DATABASE_URL no `.env`
2. Testar conexão:
   ```bash
   psql $DATABASE_URL -c "SELECT 1;"
   ```
3. Verificar se migrações foram aplicadas

### CORS Errors

1. Adicionar URL do frontend em `CORS_ORIGINS`
2. Verificar se backend está acessível
3. Verificar logs do backend

## Próximos Passos

1. ✅ Configurar Ollama localmente
2. ✅ Migrar banco para Supabase
3. ✅ Deploy frontend no Vercel
4. ✅ Deploy backend no Railway
5. ✅ Monitorar custos mensais

## Suporte

Para dúvidas ou problemas:
- Abra uma issue no GitHub
- Consulte a documentação em `SETUP.md`
- Verifique logs dos serviços

