from typing import Literal, Annotated
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
import sys
from pathlib import Path

# Adicionar diretório atual ao path
sys.path.insert(0, str(Path(__file__).parent))

from agents.supervisor import GraphState, supervisor_node, supervisor_final_node
from agents.tools import (
    OrdersTool,
    RecipesTool,
    InventoryTool,
    CalendarTool,
    PlanningTool,
)

# Instanciar tools
orders_tool = OrdersTool()
recipes_tool = RecipesTool()
inventory_tool = InventoryTool()
calendar_tool = CalendarTool()
planning_tool = PlanningTool()


def orders_node(state: GraphState) -> GraphState:
    """Nó para processar pedidos"""
    last_message = state["messages"][-1]
    
    if isinstance(last_message, HumanMessage):
        resultado = orders_tool.processar_mensagem(last_message.content)
        
        # Formatar resposta
        if resultado.get("requires_confirmation"):
            return {
                **state,
                "messages": [
                    AIMessage(content=resultado.get("confirmation_question", ""))
                ],
                "requires_confirmation": True,
                "confirmation_question": resultado.get("confirmation_question", ""),
                "next": END,
            }
        elif resultado.get("action") == "listar":
            pedidos = resultado.get("data", [])
            if pedidos and len(pedidos) > 0:
                resposta = f"Encontrei {len(pedidos)} pedido(s):\n\n"
                for pedido in pedidos[:5]:  # Limitar a 5
                    resposta += f"• Pedido #{pedido.get('id')} - {pedido.get('cliente')} - Status: {pedido.get('status')}\n"
                if len(pedidos) > 5:
                    resposta += f"\n... e mais {len(pedidos) - 5} pedido(s)"
            else:
                resposta = "Não encontrei pedidos com esses critérios."
            
            return {
                **state,
                "messages": [AIMessage(content=resposta)],
                "next": END,
            }
        else:
            return {
                **state,
                "messages": [AIMessage(content=resultado.get("message", "Processado."))],
                "next": END,
            }
    
    return {**state, "next": END}


def recipes_node(state: GraphState) -> GraphState:
    """Nó para processar receitas"""
    last_message = state["messages"][-1]
    
    if isinstance(last_message, HumanMessage):
        resultado = recipes_tool.processar_mensagem(last_message.content)
        
        if resultado.get("action") == "obter":
            receita = resultado.get("data", {})
            if "error" not in receita:
                resposta = f"**{receita.get('nome', 'Receita')}**\n\n"
                resposta += f"{receita.get('descricao', '')}\n\n" if receita.get("descricao") else ""
                resposta += f"Tempo de preparo: {receita.get('tempo_preparo', 'N/A')} minutos\n"
                resposta += f"Rendimento: {receita.get('rendimento', 'N/A')}\n\n"
                resposta += "**Ingredientes:**\n"
                for ing in receita.get("ingredientes", []):
                    resposta += f"• {ing.get('ingrediente_nome', '')}: {ing.get('quantidade')} {ing.get('unidade')}\n"
            else:
                resposta = receita.get("error", "Erro ao buscar receita")
        elif resultado.get("action") == "listar":
            receitas = resultado.get("data", [])
            resposta = f"Encontrei {len(receitas)} receita(s) no cardápio:\n\n"
            for rec in receitas[:10]:
                resposta += f"• {rec.get('nome', 'Sem nome')}\n"
        else:
            resposta = resultado.get("message", "Processado.")
        
        return {
            **state,
            "messages": [AIMessage(content=resposta)],
            "next": END,
        }
    
    return {**state, "next": END}


def inventory_node(state: GraphState) -> GraphState:
    """Nó para processar estoque"""
    last_message = state["messages"][-1]
    
    if isinstance(last_message, HumanMessage):
        resultado = inventory_tool.processar_mensagem(last_message.content)
        
        if resultado.get("action") == "calcular_custo":
            custo = resultado.get("data", {})
            resposta = f"Custo total do estoque: R$ {custo.get('custo_total', 0):.2f}\n"
            resposta += f"Total de itens: {custo.get('itens', 0)}"
        elif resultado.get("action") in ["listar", "listar_baixo"]:
            estoques = resultado.get("data", [])
            if estoques:
                resposta = f"**Estoque{' (itens críticos)' if resultado.get('action') == 'listar_baixo' else ''}:**\n\n"
                for est in estoques[:10]:
                    resposta += f"• {est.get('ingrediente_nome', '')}: {est.get('quantidade_atual')} {est.get('unidade_padrao', '')}"
                    if est.get("custo_unitario"):
                        resposta += f" (R$ {float(est.get('custo_unitario', 0)):.2f}/un)"
                    resposta += "\n"
            else:
                resposta = "Não há itens no estoque" + (" crítico" if resultado.get("action") == "listar_baixo" else "")
        else:
            resposta = resultado.get("message", "Processado.")
        
        return {
            **state,
            "messages": [AIMessage(content=resposta)],
            "next": END,
        }
    
    return {**state, "next": END}


def calendar_node(state: GraphState) -> GraphState:
    """Nó para processar agenda"""
    last_message = state["messages"][-1]
    
    if isinstance(last_message, HumanMessage):
        resultado = calendar_tool.processar_mensagem(last_message.content)
        
        if resultado.get("action") in ["listar", "listar_dia"]:
            agenda = resultado.get("data", [])
            if agenda:
                dia = resultado.get("dia", "período")
                resposta = f"**Agenda de entregas ({dia}):**\n\n"
                for entrega in agenda:
                    data_hora = entrega.get("data_hora", "")
                    cliente = entrega.get("pedido_cliente", "N/A")
                    local = entrega.get("local", "")
                    resposta += f"• {data_hora} - {cliente}"
                    if local:
                        resposta += f" ({local})"
                    resposta += "\n"
            else:
                resposta = "Não há entregas agendadas para este período."
        else:
            resposta = resultado.get("message", "Processado.")
        
        return {
            **state,
            "messages": [AIMessage(content=resposta)],
            "next": END,
        }
    
    return {**state, "next": END}


def planning_node(state: GraphState) -> GraphState:
    """Nó para processar planejamento"""
    last_message = state["messages"][-1]
    
    if isinstance(last_message, HumanMessage):
        resultado = planning_tool.processar_mensagem(last_message.content)
        
        if resultado.get("action") in ["gerar_lista", "ingredientes_pedidos"]:
            lista = resultado.get("data", {})
            if "error" not in lista:
                periodo = lista.get("periodo", {})
                resposta = f"**Lista de compras ({periodo.get('inicio')} a {periodo.get('fim')}):**\n\n"
                
                compras = lista.get("lista_compras", [])
                if compras:
                    for item in compras:
                        resposta += f"• {item.get('ingrediente', '')}: {item.get('quantidade_comprar', 0)} {item.get('unidade', '')}"
                        resposta += f" (necessário: {item.get('quantidade_necessaria', 0)}, atual: {item.get('quantidade_atual', 0)})\n"
                else:
                    resposta += "Não há necessidade de compras adicionais!"
            else:
                resposta = lista.get("error", "Erro ao gerar lista")
        else:
            resposta = resultado.get("message", "Processado.")
        
        return {
            **state,
            "messages": [AIMessage(content=resposta)],
            "next": END,
        }
    
    return {**state, "next": END}


def route_after_supervisor(state: GraphState) -> Literal["orders", "recipes", "inventory", "calendar", "planning", "supervisor_final", END]:
    """Roteia para o próximo nó baseado na decisão do supervisor"""
    next_node = state.get("next", "supervisor_final")
    
    if next_node == "supervisor":
        return "supervisor_final"
    
    return next_node


# Criar grafo
def create_graph():
    workflow = StateGraph(GraphState)
    
    # Adicionar nós
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("supervisor_final", supervisor_final_node)
    workflow.add_node("orders", orders_node)
    workflow.add_node("recipes", recipes_node)
    workflow.add_node("inventory", inventory_node)
    workflow.add_node("calendar", calendar_node)
    workflow.add_node("planning", planning_node)
    
    # Definir ponto de entrada
    workflow.set_entry_point("supervisor")
    
    # Adicionar edges condicionais
    workflow.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "orders": "orders",
            "recipes": "recipes",
            "inventory": "inventory",
            "calendar": "calendar",
            "planning": "planning",
            "supervisor_final": "supervisor_final",
            END: END,
        },
    )
    
    # Todos os nós especializados vão para END
    workflow.add_edge("orders", END)
    workflow.add_edge("recipes", END)
    workflow.add_edge("inventory", END)
    workflow.add_edge("calendar", END)
    workflow.add_edge("planning", END)
    workflow.add_edge("supervisor_final", END)
    
    return workflow.compile()


# Instância global do grafo
graph = create_graph()


def process_message(message: str, session_id: str = None) -> dict:
    """Processa uma mensagem do usuário e retorna resposta"""
    initial_state = {
        "messages": [HumanMessage(content=message)],
        "next": "supervisor",
        "requires_confirmation": False,
        "confirmation_question": "",
    }
    
    result = graph.invoke(initial_state)
    
    # Extrair última mensagem do assistente
    last_ai_message = None
    for msg in reversed(result.get("messages", [])):
        if isinstance(msg, AIMessage):
            last_ai_message = msg.content
            break
    
    return {
        "response": last_ai_message or "Desculpe, não consegui processar sua mensagem.",
        "requires_confirmation": result.get("requires_confirmation", False),
        "confirmation_question": result.get("confirmation_question", ""),
    }

