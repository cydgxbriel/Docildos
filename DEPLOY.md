# Guia de Deploy - Docildos

Este guia explica como fazer deploy do Docildos em plataformas gratuitas/baixo custo.

## Visão Geral

O Docildos pode ser deployado completamente de forma gratuita usando:

- **Frontend**: Vercel (grátis)
- **Backend**: Railway ou Render (free tier)
- **Banco de Dados**: Supabase (grátis até 500MB)
- **LLM**: Ollama (local, grátis)

## Pré-requisitos

- Conta no GitHub
- Conta no Vercel (https://vercel.com)
- Conta no Railway (https://railway.app) ou Render (https://render.com)
- Conta no Supabase (https://supabase.com)

## Deploy do Frontend (Vercel)

### Passo 1: Preparar Repositório

Certifique-se de que o código está no GitHub.

### Passo 2: Conectar no Vercel

1. Acesse https://vercel.com
2. Clique em "Add New Project"
3. Conecte seu repositório GitHub
4. Selecione o repositório Docildos

### Passo 3: Configurar Build

O Vercel detecta automaticamente Vite. Verifique:

- **Framework Preset**: Vite
- **Root Directory**: `./` (raiz)
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

### Passo 4: Variáveis de Ambiente

Adicione variável de ambiente:

- `VITE_API_URL`: URL do seu backend (será configurada após deploy do backend)
  - Exemplo: `https://docildos-backend.railway.app`

### Passo 5: Deploy

Clique em "Deploy". O Vercel fará o deploy automaticamente.

**Nota**: Após o deploy do backend, atualize `VITE_API_URL` nas configurações do projeto.

## Deploy do Backend (Railway)

### Passo 1: Criar Projeto no Railway

1. Acesse https://railway.app
2. Clique em "New Project"
3. Selecione "Deploy from GitHub repo"
4. Escolha o repositório Docildos

### Passo 2: Configurar Serviço

1. Railway detecta automaticamente o Dockerfile
2. Se não detectar, configure manualmente:
   - **Root Directory**: `/` (raiz)
   - **Dockerfile Path**: `Dockerfile`

### Passo 3: Adicionar Banco de Dados

1. Clique em "New" → "Database" → "PostgreSQL"
2. Railway criará um PostgreSQL automaticamente
3. Copie a `DATABASE_URL` das variáveis de ambiente

### Passo 4: Variáveis de Ambiente

Adicione as seguintes variáveis:

```env
DATABASE_URL=<DATABASE_URL do Railway PostgreSQL>
CORS_ORIGINS=https://seu-frontend.vercel.app
ENVIRONMENT=production
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
```

**Nota**: Para usar Supabase ao invés do PostgreSQL do Railway, substitua `DATABASE_URL` pela connection string do Supabase.

### Passo 5: Deploy

Railway fará o deploy automaticamente. Aguarde a conclusão.

### Passo 6: Obter URL do Backend

1. Após o deploy, Railway fornecerá uma URL pública
2. Exemplo: `https://docildos-backend.railway.app`
3. Copie esta URL

### Passo 7: Atualizar Frontend

Volte ao Vercel e atualize `VITE_API_URL` com a URL do backend.

## Deploy do Backend (Render - Alternativa)

### Passo 1: Criar Web Service

1. Acesse https://render.com
2. Clique em "New" → "Web Service"
3. Conecte seu repositório GitHub

### Passo 2: Configurar Build

- **Name**: `docildos-backend`
- **Environment**: `Docker`
- **Dockerfile Path**: `Dockerfile`
- **Plan**: `Free`

### Passo 3: Variáveis de Ambiente

Adicione as mesmas variáveis do Railway.

### Passo 4: Deploy

Clique em "Create Web Service". Render fará o deploy.

**Nota**: Render coloca serviços free em sleep após 15min de inatividade. Considere usar UptimeRobot para manter ativo.

## Configurar Banco de Dados (Supabase)

### Passo 1: Criar Projeto

1. Acesse https://supabase.com
2. Crie um novo projeto
3. Aguarde a criação (pode levar alguns minutos)

### Passo 2: Obter Connection String

1. Vá em "Settings" → "Database"
2. Copie a "Connection string" (URI)
3. Formato: `postgresql://postgres:[PASSWORD]@db.[PROJECT_ID].supabase.co:5432/postgres`

### Passo 3: Configurar no Backend

1. No Railway/Render, atualize `DATABASE_URL` com a connection string do Supabase
2. Formato completo:
   ```env
   DATABASE_URL=postgresql://postgres:[SUA_SENHA]@db.[PROJECT_ID].supabase.co:5432/postgres
   ```

### Passo 4: Rodar Migrações

**Opção A: Via Railway/Render Shell**

1. Abra o shell do serviço no Railway/Render
2. Execute:
   ```bash
   cd backend
   alembic upgrade head
   ```

**Opção B: Localmente**

1. Configure `DATABASE_URL` localmente apontando para Supabase
2. Execute:
   ```bash
   cd backend
   alembic upgrade head
   ```

## Configurar Ollama (LLM Local)

### Opção 1: Ollama no Mesmo Servidor (Railway/Render)

**Limitação**: Railway/Render free tier não suporta GPU, então Ollama será lento.

1. Adicione Ollama ao `docker-compose.yml` ou Dockerfile
2. Configure `OLLAMA_BASE_URL` apontando para o serviço Ollama

**Recomendação**: Use esta opção apenas para testes. Para produção, considere:

### Opção 2: Servidor Dedicado com GPU

1. Contrate um VPS com GPU (Hetzner, DigitalOcean, etc.)
2. Instale Ollama no servidor
3. Configure `OLLAMA_BASE_URL` apontando para o servidor externo
4. Configure firewall para permitir acesso apenas do backend

### Opção 3: Usar OpenAI como Fallback

Se Ollama não estiver disponível, configure:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sua_chave_aqui
```

**Nota**: Isso reintroduz custos, mas garante funcionamento.

## Verificação Pós-Deploy

### 1. Verificar Backend

```bash
curl https://seu-backend.railway.app/health
# Deve retornar: {"status": "healthy"}
```

### 2. Verificar Frontend

Acesse a URL do Vercel. A interface deve carregar.

### 3. Testar Chat

Envie uma mensagem no chat. Deve funcionar normalmente.

## Troubleshooting

### Backend não inicia

1. Verifique logs no Railway/Render
2. Verifique variáveis de ambiente
3. Verifique se `DATABASE_URL` está correto
4. Verifique se migrações foram aplicadas

### CORS Errors

1. Adicione URL do frontend em `CORS_ORIGINS`
2. Formato: `https://seu-frontend.vercel.app`
3. Reinicie o backend após alterar

### Banco de Dados não conecta

1. Verifique `DATABASE_URL` no Supabase
2. Verifique se o projeto Supabase está ativo
3. Teste conexão localmente:
   ```bash
   psql $DATABASE_URL -c "SELECT 1;"
   ```

### Ollama não responde

1. Se usando servidor externo, verifique firewall
2. Verifique se `OLLAMA_BASE_URL` está correto
3. Considere usar OpenAI como fallback temporário

## Monitoramento

### Railway

- Dashboard mostra uso de créditos
- Logs em tempo real
- Métricas de CPU/memória

### Vercel

- Analytics de uso
- Logs de build
- Métricas de performance

### Supabase

- Dashboard mostra uso de armazenamento
- Logs de queries
- Métricas de bandwidth

## Custos Finais

Com esta configuração:

- **Vercel**: $0/mês (free tier)
- **Railway**: $0-5/mês (free tier com $5 crédito)
- **Supabase**: $0/mês (free tier até 500MB)
- **Ollama**: $0/mês (se self-hosted) ou custo do VPS

**Total**: $0-5/mês (vs $35-140+/mês com serviços pagos)

## Próximos Passos

1. ✅ Configurar domínio customizado (opcional)
2. ✅ Configurar SSL (automático no Vercel/Railway)
3. ✅ Configurar monitoramento (UptimeRobot para keep-alive)
4. ✅ Configurar backups do banco (Supabase faz automaticamente)

## Suporte

Para problemas ou dúvidas:
- Consulte [COST_OPTIMIZATION.md](./COST_OPTIMIZATION.md)
- Consulte [SETUP.md](./SETUP.md)
- Abra uma issue no GitHub

