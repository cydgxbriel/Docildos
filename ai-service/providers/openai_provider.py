"""OpenAI LLM Provider - Fallback para OpenAI API"""
import os
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from .base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    """Provider para OpenAI API"""
    
    def __init__(
        self, 
        model: Optional[str] = None, 
        temperature: float = 0,
        api_key: Optional[str] = None
    ):
        super().__init__(model, temperature)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    def get_llm(self) -> BaseChatModel:
        """Retorna instância do ChatOpenAI"""
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY não configurada")
        
        return ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            api_key=self.api_key,
        )
    
    def is_available(self) -> bool:
        """Verifica se OpenAI está disponível (tem API key)"""
        return bool(self.api_key)

