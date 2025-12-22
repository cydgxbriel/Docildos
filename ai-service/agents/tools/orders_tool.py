import httpx
import os
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")


class OrdersTool:
    """Tool para operações com pedidos"""
    
    def __init__(self):
        self.base_url = f"{BACKEND_API_URL}/api/pedidos"
    
    def criar_pedido(self, pedido_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo pedido"""
        try:
            response = httpx.post(self.base_url, json=pedido_data, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Erro ao criar pedido: {str(e)}"}
    
    def listar_pedidos(
        self,
        data_inicio: str = None,
        data_fim: str = None,
        status: str = None,
        cliente: str = None,
    ) -> List[Dict[str, Any]]:
        """Lista pedidos com filtros opcionais"""
        try:
            params = {}
            if data_inicio:
                params["data_inicio"] = data_inicio
            if data_fim:
                params["data_fim"] = data_fim
            if status:
                params["status"] = status
            if cliente:
                params["cliente"] = cliente
            
            response = httpx.get(self.base_url, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return [{"error": f"Erro ao listar pedidos: {str(e)}"}]
    
    def obter_pedido(self, pedido_id: int) -> Dict[str, Any]:
        """Obtém detalhes de um pedido específico"""
        try:
            response = httpx.get(f"{self.base_url}/{pedido_id}", timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Erro ao obter pedido: {str(e)}"}
    
    def atualizar_status(self, pedido_id: int, status: str) -> Dict[str, Any]:
        """Atualiza o status de um pedido"""
        try:
            response = httpx.patch(
                f"{self.base_url}/{pedido_id}/status",
                json={"status": status},
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Erro ao atualizar status: {str(e)}"}
    
    def processar_mensagem(self, mensagem: str, contexto: Dict[str, Any] = None) -> Dict[str, Any]:
        """Processa mensagem do usuário e executa ação apropriada"""
        mensagem_lower = mensagem.lower()
        
        # Detectar intenção
        if "criar" in mensagem_lower or "novo pedido" in mensagem_lower:
            # Extrair informações do pedido (será melhorado com LLM)
            return {
                "action": "criar",
                "requires_confirmation": True,
                "confirmation_question": "Preciso de mais informações para criar o pedido. Pode me informar: cliente, itens (receita e quantidade), data de entrega e horário?",
            }
        
        elif "listar" in mensagem_lower or "mostrar" in mensagem_lower or "pedidos" in mensagem_lower:
            # Extrair filtros
            filtros = {}
            if "hoje" in mensagem_lower:
                from datetime import date
                filtros["data_inicio"] = str(date.today())
                filtros["data_fim"] = str(date.today())
            elif "semana" in mensagem_lower:
                from datetime import date, timedelta
                hoje = date.today()
                fim_semana = hoje + timedelta(days=7)
                filtros["data_inicio"] = str(hoje)
                filtros["data_fim"] = str(fim_semana)
            
            if "novo" in mensagem_lower:
                filtros["status"] = "novo"
            elif "produção" in mensagem_lower:
                filtros["status"] = "em_producao"
            elif "pronto" in mensagem_lower:
                filtros["status"] = "pronto"
            
            pedidos = self.listar_pedidos(**filtros)
            return {
                "action": "listar",
                "data": pedidos,
            }
        
        elif "status" in mensagem_lower or "marcar" in mensagem_lower:
            # Tentar extrair ID do pedido e novo status
            return {
                "action": "atualizar_status",
                "requires_confirmation": True,
                "confirmation_question": "Qual pedido você quer atualizar e para qual status? (novo, em_producao, pronto, entregue)",
            }
        
        else:
            return {
                "action": "consulta",
                "message": "Não entendi o que você quer fazer com pedidos. Pode reformular?",
            }

