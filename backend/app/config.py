"""Configuração centralizada do Backend"""
import os
from pydantic_settings import BaseSettings
from typing import List


class BackendConfig(BaseSettings):
    """Configurações do Backend"""
    
    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://docildos:docildos_dev@localhost:5432/docildos_db"
    )
    
    # CORS
    cors_origins: List[str] = [
        origin.strip() 
        for origin in os.getenv(
            "CORS_ORIGINS", 
            "http://localhost:8080,http://localhost:5173"
        ).split(",")
        if origin.strip()
    ]
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # API Info
    api_title: str = "Docildos API"
    api_description: str = "API para gestão de confeitaria com IA"
    api_version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instância global de configuração
config = BackendConfig()

