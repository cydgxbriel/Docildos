"""Factory para criar instâncias de LLM providers"""
import os
from typing import Optional
from .base import BaseLLMProvider
from .ollama_provider import OllamaProvider
from .openai_provider import OpenAIProvider


def get_llm_provider(
    provider: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0
) -> BaseLLMProvider:
    """
    Factory function para criar instância do provider de LLM
    
    Args:
        provider: Nome do provider ('ollama', 'openai'). Se None, usa LLM_PROVIDER do env
        model: Nome do modelo a usar
        temperature: Temperatura para o modelo
    
    Returns:
        Instância do provider configurado
    
    Raises:
        ValueError: Se o provider não for suportado ou não estiver disponível
    """
    provider = provider or os.getenv("LLM_PROVIDER", "ollama").lower()
    
    if provider == "ollama":
        ollama_provider = OllamaProvider(model=model, temperature=temperature)
        if ollama_provider.is_available():
            return ollama_provider
        else:
            # Fallback para OpenAI se Ollama não estiver disponível
            print("⚠️  Ollama não disponível, tentando OpenAI como fallback...")
            provider = "openai"
    
    if provider == "openai":
        openai_provider = OpenAIProvider(model=model, temperature=temperature)
        if openai_provider.is_available():
            return openai_provider
        else:
            raise ValueError(
                "OpenAI não disponível. Configure OPENAI_API_KEY ou inicie o Ollama."
            )
    
    raise ValueError(f"Provider '{provider}' não suportado. Use 'ollama' ou 'openai'.")

