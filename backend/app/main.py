from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router

app = FastAPI(
    title="Docildos API",
    description="API para gestão de confeitaria com IA",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:5173"],
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

