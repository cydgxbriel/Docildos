"""Configuração centralizada do AI Service"""
import os
from pydantic_settings import BaseSettings
from typing import Optional


class AIServiceConfig(BaseSettings):
    """Configurações do AI Service"""
    
    # LLM Provider
    llm_provider: str = os.getenv("LLM_PROVIDER", "ollama")
    llm_model: Optional[str] = os.getenv("LLM_MODEL")
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0"))
    
    # Ollama
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3")
    
    # OpenAI (fallback)
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Backend API
    backend_api_url: str = os.getenv("BACKEND_API_URL", "http://localhost:8000")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instância global de configuração
config = AIServiceConfig()

