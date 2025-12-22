from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import date, datetime
from app.db.database import get_db
from app.models.pedido import Pedido, StatusPedido
from app.models.agenda import AgendaEntrega
from app.models.estoque import Estoque
from app.schemas.stats import StatsResponse

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("", response_model=StatsResponse)
def obter_stats(db: Session = Depends(get_db)):
    hoje = date.today()
    
    # Pedidos de hoje
    pedidos_hoje = (
        db.query(Pedido).filter(Pedido.data_entrega == hoje).count()
    )
    
    # Pedidos novos de hoje
    pedidos_novos = (
        db.query(Pedido)
        .filter(
            and_(
                Pedido.data_entrega == hoje,
                Pedido.status == StatusPedido.NOVO,
            )
        )
        .count()
    )
    
    # Entregas pendentes (agendadas para hoje ou futuro)
    agora = datetime.now()
    entregas_pendentes = (
        db.query(AgendaEntrega)
        .filter(AgendaEntrega.data_hora >= agora)
        .count()
    )
    
    # Em produção
    em_producao = (
        db.query(Pedido)
        .filter(Pedido.status == StatusPedido.EM_PRODUCAO)
        .count()
    )
    
    # Estoque baixo (quantidade atual <= ponto de reposição)
    estoque_baixo = (
        db.query(Estoque)
        .filter(Estoque.quantidade_atual <= Estoque.ponto_reposicao)
        .count()
    )
    
    # Total de pedidos de hoje (soma dos preços)
    total_pedidos_hoje = (
        db.query(func.sum(Pedido.preco_total))
        .filter(Pedido.data_entrega == hoje)
        .scalar()
    )
    
    return StatsResponse(
        pedidos_hoje=pedidos_hoje,
        pedidos_novos=pedidos_novos,
        entregas_pendentes=entregas_pendentes,
        em_producao=em_producao,
        estoque_baixo=estoque_baixo,
        total_pedidos_hoje=total_pedidos_hoje,
    )

