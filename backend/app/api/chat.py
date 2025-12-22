from fastapi import APIRouter, Depends
import sys
import os
from pathlib import Path

# Adicionar ai-service ao path
project_root = Path(__file__).parent.parent.parent.parent
ai_service_path = project_root / "ai-service"
if ai_service_path.exists():
    sys.path.insert(0, str(ai_service_path))

from app.schemas.chat import ChatMessage, ChatResponse

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def processar_chat(message: ChatMessage):
    try:
        # Tentar importar o graph do ai-service
        try:
            from graph import process_message
        except ImportError:
            # Fallback: retornar resposta simples se ai-service não estiver disponível
            return ChatResponse(
                response="Olá! Sou sua assistente de confeitaria. O serviço de IA está sendo configurado. Por enquanto, você pode usar os endpoints da API diretamente.",
                cards=None,
                actions=None,
                requires_confirmation=False,
            )
        
        resultado = process_message(message.message, message.session_id)
        
        return ChatResponse(
            response=resultado["response"],
            cards=None,
            actions=None,
            requires_confirmation=resultado.get("requires_confirmation", False),
            confirmation_question=resultado.get("confirmation_question"),
        )
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Erro no chat: {error_details}")  # Log para debug
        return ChatResponse(
            response=f"Desculpe, ocorreu um erro ao processar sua mensagem. Verifique os logs do servidor para mais detalhes.",
            cards=None,
            actions=None,
            requires_confirmation=False,
        )

