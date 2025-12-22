import httpx
import os
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")


class RecipesTool:
    """Tool para operações com receitas"""
    
    def __init__(self):
        self.base_url = f"{BACKEND_API_URL}/api/receitas"
    
    def listar_receitas(self, nome: str = None) -> List[Dict[str, Any]]:
        """Lista receitas, opcionalmente filtradas por nome"""
        try:
            params = {}
            if nome:
                params["nome"] = nome
            
            response = httpx.get(self.base_url, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return [{"error": f"Erro ao listar receitas: {str(e)}"}]
    
    def obter_receita(self, receita_id: int) -> Dict[str, Any]:
        """Obtém detalhes de uma receita específica"""
        try:
            response = httpx.get(f"{self.base_url}/{receita_id}", timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Erro ao obter receita: {str(e)}"}
    
    def buscar_receita_por_nome(self, nome: str) -> Dict[str, Any]:
        """Busca receita por nome (retorna primeira correspondência)"""
        receitas = self.listar_receitas(nome=nome)
        if receitas and len(receitas) > 0:
            # Buscar receita completa
            return self.obter_receita(receitas[0]["id"])
        return {"error": f"Receita '{nome}' não encontrada"}
    
    def processar_mensagem(self, mensagem: str, contexto: Dict[str, Any] = None) -> Dict[str, Any]:
        """Processa mensagem do usuário e executa ação apropriada"""
        mensagem_lower = mensagem.lower()
        
        # Detectar intenção
        if "ficha" in mensagem_lower or "receita" in mensagem_lower or "cardápio" in mensagem_lower:
            # Tentar extrair nome da receita
            palavras = mensagem.split()
            receita_nome = None
            
            # Procurar por padrões como "ficha do X", "receita X", "X 500g"
            for i, palavra in enumerate(palavras):
                if palavra.lower() in ["do", "da", "de"] and i + 1 < len(palavras):
                    receita_nome = " ".join(palavras[i + 1:])
                    break
            
            if not receita_nome:
                # Tentar pegar palavras após "receita" ou "ficha"
                for i, palavra in enumerate(palavras):
                    if palavra.lower() in ["receita", "ficha"] and i + 1 < len(palavras):
                        receita_nome = " ".join(palavras[i + 1:])
                        break
            
            if receita_nome:
                receita = self.buscar_receita_por_nome(receita_nome.strip())
                return {
                    "action": "obter",
                    "data": receita,
                }
            else:
                # Listar todas as receitas
                receitas = self.listar_receitas()
                return {
                    "action": "listar",
                    "data": receitas,
                }
        
        else:
            return {
                "action": "consulta",
                "message": "Não entendi o que você quer fazer com receitas. Pode reformular?",
            }

