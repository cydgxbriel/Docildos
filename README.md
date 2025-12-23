# Docildos

Sistema de gestão de confeitaria com inteligência artificial, desenvolvido para auxiliar na administração de pedidos, receitas, estoque e planejamento de produção.

## 🎯 Sobre o Projeto

Docildos é uma aplicação full-stack que combina uma interface moderna em React com uma API robusta em FastAPI e um serviço de IA baseado em LangGraph para orquestração de agentes. O sistema permite gerenciar todos os aspectos de uma confeitaria através de uma interface conversacional intuitiva.

### 💰 Otimização de Custos

O Docildos foi projetado para operar com **custos mínimos** usando serviços open source:

- **LLM Local Gratuito**: Usa Ollama (LLM local) por padrão, eliminando custos de API OpenAI
- **Hosting Gratuito**: Configurado para Railway, Render, Vercel (free tiers)
- **Banco Gratuito**: Suporte para Supabase, Neon, Railway PostgreSQL (free tiers)

**Economia estimada**: $35-135+/mês → $0-5/mês (95-100% de redução)

Consulte [COST_OPTIMIZATION.md](./COST_OPTIMIZATION.md) para detalhes completos.

## 🚀 Tecnologias

### Frontend
- **React 18** - Biblioteca JavaScript para construção de interfaces
- **TypeScript** - Tipagem estática para JavaScript
- **Vite** - Build tool e dev server
- **shadcn/ui** - Componentes de UI acessíveis
- **Tailwind CSS** - Framework CSS utility-first
- **React Router** - Roteamento para aplicações React
- **TanStack Query** - Gerenciamento de estado do servidor
- **React Hook Form** - Gerenciamento de formulários
- **Zod** - Validação de schemas

### Backend
- **FastAPI** - Framework web moderno e rápido para Python
- **SQLAlchemy** - ORM para Python
- **Alembic** - Ferramenta de migração de banco de dados
- **Pydantic** - Validação de dados usando type hints
- **PostgreSQL** - Banco de dados relacional

### AI Service
- **LangGraph** - Framework para construção de aplicações com LLMs
- **Ollama** - LLM local gratuito (padrão)
- **OpenAI API** - Integração opcional com modelos de linguagem (fallback)

### Infraestrutura
- **Docker** - Containerização do banco de dados
- **Docker Compose** - Orquestração de containers

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Node.js** (versão 18 ou superior) e npm
- **Python** (versão 3.10 ou superior)
- **Docker** e Docker Compose (para desenvolvimento local)
- **Git**

**Nota**: Para produção com custos mínimos, você pode usar serviços gerenciados (Railway, Supabase) que não requerem Docker local.

## 🛠️ Instalação e Configuração

Para um guia detalhado de instalação, consulte o arquivo [SETUP.md](./SETUP.md).

### Passo a Passo Rápido

1. **Clone o repositório**
```bash
git clone https://github.com/cydgxbriel/Docildos.git
cd Docildos
```

2. **Configure o banco de dados**
```bash
docker-compose up -d postgres
```

Aguarde aproximadamente 10 segundos para o PostgreSQL inicializar.

3. **Configure o Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edite o arquivo .env com suas configurações, especialmente OPENAI_API_KEY
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

4. **Configure o AI Service** (em outro terminal)
```bash
cd ai-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edite o arquivo .env com OPENAI_API_KEY e BACKEND_API_URL=http://localhost:8000
```

5. **Configure o Frontend** (em outro terminal)
```bash
npm install
npm run dev
```

## ✅ Verificação

Após seguir os passos acima, verifique se tudo está funcionando:

1. **Backend**: Acesse http://localhost:8000/docs para ver a documentação interativa da API
2. **Frontend**: Acesse http://localhost:8080 (ou a porta indicada no terminal)
3. **Teste o chat**: Tente enviar uma mensagem como "Me mostra os pedidos de hoje"

## 📁 Estrutura do Projeto

```
Docildos/
├── ai-service/          # Serviço de IA com LangGraph
│   ├── agents/         # Agentes e ferramentas
│   └── graph.py        # Grafo LangGraph principal
├── backend/            # API FastAPI
│   ├── app/
│   │   ├── api/        # Endpoints REST
│   │   ├── models/     # Modelos SQLAlchemy
│   │   ├── schemas/    # Schemas Pydantic
│   │   ├── services/   # Lógica de negócio
│   │   └── db/         # Configuração do banco
│   └── alembic/        # Migrações do banco
├── src/                # Código fonte do frontend
│   ├── components/     # Componentes React
│   ├── pages/          # Páginas da aplicação
│   ├── hooks/          # Custom hooks
│   └── lib/            # Utilitários
├── public/             # Arquivos estáticos
└── docker-compose.yml  # Configuração Docker
```

## 🔧 Scripts Disponíveis

### Frontend
- `npm run dev` - Inicia o servidor de desenvolvimento
- `npm run build` - Cria build de produção
- `npm run lint` - Executa o linter
- `npm run preview` - Preview do build de produção

### Backend
- `uvicorn app.main:app --reload` - Inicia o servidor de desenvolvimento
- `alembic upgrade head` - Aplica migrações do banco
- `alembic revision --autogenerate -m "descrição"` - Cria nova migração

## 🐛 Solução de Problemas

### Erro de conexão com banco de dados
- Verifique se o Docker está rodando: `docker ps`
- Verifique se o PostgreSQL está ativo: `docker-compose ps`
- Confirme as credenciais no arquivo `.env` do backend

### Erro de importação no backend
- Certifique-se de que o `ai-service` está no mesmo nível que `backend`
- Verifique se todas as dependências estão instaladas nos ambientes virtuais

### Erro de CORS
- Verifique se o frontend está usando a porta correta (8080 ou 5173)
- Adicione a porta no CORS do backend se necessário (arquivo `main.py`)

### Reconhecimento de voz não funciona
- Use Chrome ou Edge para melhor suporte à Web Speech API
- Verifique as permissões do microfone no navegador

## 📝 Variáveis de Ambiente

### Backend (.env)
```env
DATABASE_URL=postgresql://docildos:docildos_dev@localhost:5432/docildos_db
CORS_ORIGINS=http://localhost:8080,http://localhost:5173
ENVIRONMENT=development
```

### AI Service (.env)
```env
# LLM Provider: 'ollama' (gratuito, padrão) ou 'openai' (pago)
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:8b

# OpenAI (opcional, apenas se LLM_PROVIDER=openai)
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-4o-mini

BACKEND_API_URL=http://localhost:8000
```

**Importante**: Por padrão, o sistema usa **Ollama (gratuito)**. Para usar OpenAI, configure `LLM_PROVIDER=openai` e `OPENAI_API_KEY`.

Consulte os arquivos `.env.example` em cada diretório para exemplos completos.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## 📄 Licença

Este projeto está sob a licença MIT.

## 👤 Autor

**cydgxbriel**

## 🔗 Links Úteis

- [Documentação do FastAPI](https://fastapi.tiangolo.com/)
- [Documentação do React](https://react.dev/)
- [Documentação do LangGraph](https://langchain-ai.github.io/langgraph/)
- [Documentação do shadcn/ui](https://ui.shadcn.com/)
