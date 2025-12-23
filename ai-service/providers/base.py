"""Base class for LLM providers"""
from abc import ABC, abstractmethod
from langchain_core.language_models import BaseChatModel
from typing import Optional


class BaseLLMProvider(ABC):
    """Interface base para provedores de LLM"""
    
    def __init__(self, model: Optional[str] = None, temperature: float = 0):
        self.model = model
        self.temperature = temperature
    
    @abstractmethod
    def get_llm(self) -> BaseChatModel:
        """Retorna uma instância do LLM configurado"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Verifica se o provider está disponível"""
        pass

