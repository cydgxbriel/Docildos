"""Ollama LLM Provider - LLM local gratuito"""
import os
from typing import Optional
from langchain_ollama import ChatOllama
from langchain_core.language_models import BaseChatModel
from .base import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):
    """Provider para Ollama (LLM local)"""
    
    def __init__(
        self, 
        model: Optional[str] = None, 
        temperature: float = 0,
        base_url: Optional[str] = None
    ):
        super().__init__(model, temperature)
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3")
    
    def get_llm(self) -> BaseChatModel:
        """Retorna instância do ChatOllama"""
        return ChatOllama(
            model=self.model,
            temperature=self.temperature,
            base_url=self.base_url,
        )
    
    def is_available(self) -> bool:
        """Verifica se Ollama está disponível"""
        try:
            import httpx
            response = httpx.get(f"{self.base_url}/api/tags", timeout=2.0)
            return response.status_code == 200
        except Exception:
            return False

