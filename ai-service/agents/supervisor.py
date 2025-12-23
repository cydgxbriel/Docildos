from typing import Literal, Annotated
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
import os
from dotenv import load_dotenv
import sys
from pathlib import Path

# Carregar variáveis de ambiente primeiro
load_dotenv()

# Adicionar diretório pai ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from providers.factory import get_llm_provider
from config import config

# Tipos de nós do grafo
NodeType = Literal[
    "orders",
    "recipes",
    "inventory",
    "calendar",
    "planning",
    "supervisor",
]

# Estado do grafo
class GraphState:
    messages: Annotated[list, add_messages]
    next: str
    requires_confirmation: bool = False
    confirmation_question: str = ""

# Modelo LLM - Usa provider abstraction (Ollama por padrão, OpenAI como fallback)
try:
    llm_provider = get_llm_provider(
        provider=config.llm_provider,
        model=config.llm_model,
        temperature=config.llm_temperature
    )
    llm = llm_provider.get_llm()
    print(f"✅ LLM Provider configurado: {config.llm_provider}")
except Exception as e:
    print(f"❌ Erro ao configurar LLM provider: {e}")
    raise

# Prompt do supervisor
SUPERVISOR_PROMPT = """Você é um supervisor inteligente que analisa mensagens de usuários e decide qual ferramenta especializada deve ser chamada.

Ferramentas disponíveis:
- orders: Para criar, consultar, atualizar status de pedidos
- recipes: Para consultar receitas, cardápio, fichas técnicas
- inventory: Para consultar estoque, custos, movimentações
- calendar: Para consultar agenda de entregas, agendar entregas
- planning: Para planejamento de ingredientes, lista de compras, explosão de BOM

Analise a mensagem do usuário e responda APENAS com o nome da ferramenta mais apropriada (orders, recipes, inventory, calendar, planning).
Se a mensagem não se encaixar em nenhuma categoria, responda "supervisor" para que eu possa responder diretamente.

Mensagem do usuário: {user_message}
"""

def supervisor_node(state: GraphState) -> GraphState:
    """Nó supervisor que decide qual tool chamar"""
    last_message = state["messages"][-1]
    
    if isinstance(last_message, HumanMessage):
        user_message = last_message.content
        
        # Chamar LLM para decidir
        response = llm.invoke(
            SystemMessage(content=SUPERVISOR_PROMPT.format(user_message=user_message))
        )
        
        tool_name = response.content.strip().lower()
        
        # Validar tool_name
        valid_tools = ["orders", "recipes", "inventory", "calendar", "planning", "supervisor"]
        if tool_name not in valid_tools:
            tool_name = "supervisor"
        
        return {
            **state,
            "next": tool_name,
        }
    
    return {**state, "next": "supervisor"}

def supervisor_final_node(state: GraphState) -> GraphState:
    """Nó final que responde quando não há tool específica"""
    last_message = state["messages"][-1]
    
    if isinstance(last_message, HumanMessage):
        response = llm.invoke([
            SystemMessage(content="Você é uma assistente de confeitaria amigável e prestativa. Responda de forma natural e útil."),
            last_message
        ])
        
        return {
            **state,
            "messages": [AIMessage(content=response.content)],
            "next": END,
        }
    
    return {**state, "next": END}

# Criar grafo
def create_supervisor_graph():
    workflow = StateGraph(GraphState)
    
    # Adicionar nós
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("supervisor_final", supervisor_final_node)
    
    # Adicionar edges condicionais (serão adicionados quando as tools forem criadas)
    workflow.set_entry_point("supervisor")
    
    return workflow

