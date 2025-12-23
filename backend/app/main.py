from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.config import config

app = FastAPI(
    title=config.api_title,
    description=config.api_description,
    version=config.api_version
)

# CORS - Configurável via variável de ambiente
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Docildos API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

