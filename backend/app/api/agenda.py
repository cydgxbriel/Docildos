from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from app.db.database import get_db
from app.models.agenda import AgendaEntrega
from app.models.pedido import Pedido
from app.schemas.agenda import (
    AgendaEntregaCreate,
    AgendaEntregaUpdate,
    AgendaEntregaResponse,
)

router = APIRouter(prefix="/api/agenda", tags=["agenda"])


@router.get("", response_model=List[AgendaEntregaResponse])
def listar_agenda(
    data_inicio: Optional[date] = Query(None),
    data_fim: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(AgendaEntrega)
    
    if data_inicio:
        query = query.filter(AgendaEntrega.data_hora >= datetime.combine(data_inicio, datetime.min.time()))
    if data_fim:
        query = query.filter(AgendaEntrega.data_hora <= datetime.combine(data_fim, datetime.max.time()))
    
    entregas = query.order_by(AgendaEntrega.data_hora.asc()).all()
    
    result = []
    for entrega in entregas:
        pedido = db.query(Pedido).filter(Pedido.id == entrega.pedido_id).first()
        result.append(
            AgendaEntregaResponse(
                id=entrega.id,
                pedido_id=entrega.pedido_id,
                data_hora=entrega.data_hora,
                local=entrega.local,
                responsavel=entrega.responsavel,
                pedido_cliente=pedido.cliente if pedido else None,
            )
        )
    return result


@router.post("", response_model=AgendaEntregaResponse, status_code=201)
def criar_agenda(agenda_data: AgendaEntregaCreate, db: Session = Depends(get_db)):
    # Verificar se pedido existe
    pedido = db.query(Pedido).filter(Pedido.id == agenda_data.pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    # Verificar se já existe agenda para este pedido
    agenda_existente = (
        db.query(AgendaEntrega)
        .filter(AgendaEntrega.pedido_id == agenda_data.pedido_id)
        .first()
    )
    if agenda_existente:
        raise HTTPException(
            status_code=400, detail="Já existe uma agenda para este pedido"
        )
    
    agenda = AgendaEntrega(
        pedido_id=agenda_data.pedido_id,
        data_hora=agenda_data.data_hora,
        local=agenda_data.local,
        responsavel=agenda_data.responsavel,
    )
    db.add(agenda)
    db.commit()
    db.refresh(agenda)
    
    return AgendaEntregaResponse(
        id=agenda.id,
        pedido_id=agenda.pedido_id,
        data_hora=agenda.data_hora,
        local=agenda.local,
        responsavel=agenda.responsavel,
        pedido_cliente=pedido.cliente,
    )


@router.patch("/{agenda_id}", response_model=AgendaEntregaResponse)
def atualizar_agenda(
    agenda_id: int, agenda_data: AgendaEntregaUpdate, db: Session = Depends(get_db)
):
    agenda = db.query(AgendaEntrega).filter(AgendaEntrega.id == agenda_id).first()
    if not agenda:
        raise HTTPException(status_code=404, detail="Agenda não encontrada")
    
    update_data = agenda_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agenda, field, value)
    
    db.commit()
    db.refresh(agenda)
    
    pedido = db.query(Pedido).filter(Pedido.id == agenda.pedido_id).first()
    
    return AgendaEntregaResponse(
        id=agenda.id,
        pedido_id=agenda.pedido_id,
        data_hora=agenda.data_hora,
        local=agenda.local,
        responsavel=agenda.responsavel,
        pedido_cliente=pedido.cliente if pedido else None,
    )

