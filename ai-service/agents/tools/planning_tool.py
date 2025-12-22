import httpx
import os
from typing import Dict, Any, List
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")


class PlanningTool:
    """Tool para planejamento de ingredientes e lista de compras"""
    
    def __init__(self):
        self.pedidos_url = f"{BACKEND_API_URL}/api/pedidos"
        self.receitas_url = f"{BACKEND_API_URL}/api/receitas"
        self.estoque_url = f"{BACKEND_API_URL}/api/estoque"
    
    def gerar_lista_compras(
        self, data_inicio: str = None, data_fim: str = None
    ) -> Dict[str, Any]:
        """Gera lista de compras consolidada para um período"""
        try:
            # Buscar pedidos do período
            params = {}
            if data_inicio:
                params["data_inicio"] = data_inicio
            if data_fim:
                params["data_fim"] = data_fim
            
            response = httpx.get(self.pedidos_url, params=params, timeout=10.0)
            response.raise_for_status()
            pedidos = response.json()
            
            # Consolidar ingredientes
            ingredientes_necessarios = {}
            
            for pedido in pedidos:
                if "itens" in pedido:
                    for item in pedido["itens"]:
                        receita_id = item.get("receita_id")
                        quantidade_item = item.get("quantidade", 1)
                        
                        # Buscar receita
                        rec_response = httpx.get(
                            f"{self.receitas_url}/{receita_id}", timeout=10.0
                        )
                        if rec_response.status_code == 200:
                            receita = rec_response.json()
                            
                            # Multiplicar ingredientes pela quantidade do item
                            if "ingredientes" in receita:
                                for ing in receita["ingredientes"]:
                                    ing_id = ing.get("ingrediente_id")
                                    qtd = float(ing.get("quantidade", 0)) * quantidade_item
                                    unidade = ing.get("unidade", "g")
                                    
                                    key = f"{ing_id}_{unidade}"
                                    if key not in ingredientes_necessarios:
                                        ingredientes_necessarios[key] = {
                                            "ingrediente_id": ing_id,
                                            "quantidade": 0,
                                            "unidade": unidade,
                                            "ingrediente_nome": ing.get("ingrediente_nome"),
                                        }
                                    ingredientes_necessarios[key]["quantidade"] += qtd
            
            # Buscar estoque atual e calcular o que falta
            estoque_response = httpx.get(self.estoque_url, timeout=10.0)
            estoques = {}
            if estoque_response.status_code == 200:
                for estoque in estoque_response.json():
                    estoques[estoque["ingrediente_id"]] = estoque
            
            lista_compras = []
            for ing_data in ingredientes_necessarios.values():
                ing_id = ing_data["ingrediente_id"]
                qtd_necessaria = ing_data["quantidade"]
                qtd_atual = 0
                
                if ing_id in estoques:
                    qtd_atual = float(estoques[ing_id].get("quantidade_atual", 0))
                
                qtd_comprar = max(0, qtd_necessaria - qtd_atual)
                
                if qtd_comprar > 0:
                    lista_compras.append({
                        "ingrediente": ing_data["ingrediente_nome"],
                        "quantidade_necessaria": qtd_necessaria,
                        "quantidade_atual": qtd_atual,
                        "quantidade_comprar": qtd_comprar,
                        "unidade": ing_data["unidade"],
                    })
            
            return {
                "periodo": {
                    "inicio": data_inicio or str(date.today()),
                    "fim": data_fim or str(date.today() + timedelta(days=7)),
                },
                "lista_compras": lista_compras,
            }
            
        except Exception as e:
            return {"error": f"Erro ao gerar lista de compras: {str(e)}"}
    
    def processar_mensagem(self, mensagem: str, contexto: Dict[str, Any] = None) -> Dict[str, Any]:
        """Processa mensagem do usuário e executa ação apropriada"""
        mensagem_lower = mensagem.lower()
        
        # Detectar intenção
        if "lista" in mensagem_lower and "compra" in mensagem_lower:
            # Tentar extrair período
            hoje = date.today()
            data_inicio = None
            data_fim = None
            
            if "amanhã" in mensagem_lower or "amanha" in mensagem_lower:
                data_inicio = str(hoje + timedelta(days=1))
                data_fim = str(hoje + timedelta(days=1))
            elif "semana" in mensagem_lower:
                data_inicio = str(hoje)
                data_fim = str(hoje + timedelta(days=7))
            elif "hoje" in mensagem_lower:
                data_inicio = str(hoje)
                data_fim = str(hoje)
            
            lista = self.gerar_lista_compras(data_inicio=data_inicio, data_fim=data_fim)
            return {
                "action": "gerar_lista",
                "data": lista,
            }
        
        elif "ingrediente" in mensagem_lower and ("pedido" in mensagem_lower or "necessário" in mensagem_lower or "preciso" in mensagem_lower):
            # Similar à lista de compras
            hoje = date.today()
            lista = self.gerar_lista_compras(
                data_inicio=str(hoje), data_fim=str(hoje + timedelta(days=1))
            )
            return {
                "action": "ingredientes_pedidos",
                "data": lista,
            }
        
        else:
            return {
                "action": "consulta",
                "message": "Não entendi o que você quer fazer com planejamento. Pode reformular?",
            }

