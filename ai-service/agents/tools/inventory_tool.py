import httpx
import os
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")


class InventoryTool:
    """Tool para operações com estoque"""
    
    def __init__(self):
        self.base_url = f"{BACKEND_API_URL}/api/estoque"
    
    def listar_estoque(self, ingrediente_id: int = None, baixo_estoque: bool = None) -> List[Dict[str, Any]]:
        """Lista estoque, opcionalmente filtrado"""
        try:
            params = {}
            if ingrediente_id:
                params["ingrediente_id"] = ingrediente_id
            if baixo_estoque is not None:
                params["baixo_estoque"] = baixo_estoque
            
            response = httpx.get(self.base_url, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return [{"error": f"Erro ao listar estoque: {str(e)}"}]
    
    def obter_estoque_ingrediente(self, ingrediente_id: int) -> Dict[str, Any]:
        """Obtém estoque de um ingrediente específico"""
        try:
            response = httpx.get(f"{self.base_url}/{ingrediente_id}", timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Erro ao obter estoque: {str(e)}"}
    
    def calcular_custo_total(self) -> Dict[str, Any]:
        """Calcula custo total do estoque"""
        estoques = self.listar_estoque()
        total = 0.0
        
        for estoque in estoques:
            if estoque.get("custo_unitario") and estoque.get("quantidade_atual"):
                total += float(estoque["custo_unitario"]) * float(estoque["quantidade_atual"])
        
        return {
            "custo_total": total,
            "itens": len(estoques),
        }
    
    def processar_mensagem(self, mensagem: str, contexto: Dict[str, Any] = None) -> Dict[str, Any]:
        """Processa mensagem do usuário e executa ação apropriada"""
        mensagem_lower = mensagem.lower()
        
        # Detectar intenção
        if "estoque" in mensagem_lower or "tenho" in mensagem_lower or "quanto" in mensagem_lower:
            if "baixo" in mensagem_lower or "crítico" in mensagem_lower or "faltando" in mensagem_lower:
                estoques = self.listar_estoque(baixo_estoque=True)
                return {
                    "action": "listar_baixo",
                    "data": estoques,
                }
            elif "custo" in mensagem_lower or "valor" in mensagem_lower:
                custo = self.calcular_custo_total()
                return {
                    "action": "calcular_custo",
                    "data": custo,
                }
            else:
                # Listar todo o estoque
                estoques = self.listar_estoque()
                return {
                    "action": "listar",
                    "data": estoques,
                }
        
        else:
            return {
                "action": "consulta",
                "message": "Não entendi o que você quer fazer com estoque. Pode reformular?",
            }

