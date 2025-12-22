from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.db.database import get_db
from app.models.pedido import Pedido, ItemPedido, StatusPedido
from app.models.receita import Receita
from app.schemas.pedido import (
    PedidoCreate,
    PedidoUpdate,
    PedidoResponse,
    PedidoStatusUpdate,
    ItemPedidoResponse,
)

router = APIRouter(prefix="/api/pedidos", tags=["pedidos"])


@router.get("", response_model=List[PedidoResponse])
def listar_pedidos(
    data_inicio: Optional[date] = Query(None),
    data_fim: Optional[date] = Query(None),
    status: Optional[StatusPedido] = Query(None),
    cliente: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Pedido)
    
    if data_inicio:
        query = query.filter(Pedido.data_entrega >= data_inicio)
    if data_fim:
        query = query.filter(Pedido.data_entrega <= data_fim)
    if status:
        query = query.filter(Pedido.status == status)
    if cliente:
        query = query.filter(Pedido.cliente.ilike(f"%{cliente}%"))
    
    pedidos = query.order_by(Pedido.data_entrega.desc()).all()
    
    result = []
    for pedido in pedidos:
        itens_response = []
        for item in pedido.itens:
            receita = db.query(Receita).filter(Receita.id == item.receita_id).first()
            itens_response.append(
                ItemPedidoResponse(
                    id=item.id,
                    receita_id=item.receita_id,
                    quantidade=item.quantidade,
                    unidade=item.unidade,
                    personalizacoes=item.personalizacoes,
                    receita_nome=receita.nome if receita else None,
                )
            )
        result.append(
            PedidoResponse(
                id=pedido.id,
                cliente=pedido.cliente,
                status=pedido.status,
                data_entrega=pedido.data_entrega,
                horario=pedido.horario,
                local=pedido.local,
                observacoes=pedido.observacoes,
                preco_total=pedido.preco_total,
                itens=itens_response,
            )
        )
    return result


@router.get("/{pedido_id}", response_model=PedidoResponse)
def obter_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    itens_response = []
    for item in pedido.itens:
        receita = db.query(Receita).filter(Receita.id == item.receita_id).first()
        itens_response.append(
            ItemPedidoResponse(
                id=item.id,
                receita_id=item.receita_id,
                quantidade=item.quantidade,
                unidade=item.unidade,
                personalizacoes=item.personalizacoes,
                receita_nome=receita.nome if receita else None,
            )
        )
    
    return PedidoResponse(
        id=pedido.id,
        cliente=pedido.cliente,
        status=pedido.status,
        data_entrega=pedido.data_entrega,
        horario=pedido.horario,
        local=pedido.local,
        observacoes=pedido.observacoes,
        preco_total=pedido.preco_total,
        itens=itens_response,
    )


@router.post("", response_model=PedidoResponse, status_code=201)
def criar_pedido(pedido_data: PedidoCreate, db: Session = Depends(get_db)):
    # Criar pedido
    pedido = Pedido(
        cliente=pedido_data.cliente,
        status=StatusPedido.NOVO,
        data_entrega=pedido_data.data_entrega,
        horario=pedido_data.horario,
        local=pedido_data.local,
        observacoes=pedido_data.observacoes,
        preco_total=pedido_data.preco_total,
    )
    db.add(pedido)
    db.flush()
    
    # Criar itens
    for item_data in pedido_data.itens:
        item = ItemPedido(
            pedido_id=pedido.id,
            receita_id=item_data.receita_id,
            quantidade=item_data.quantidade,
            unidade=item_data.unidade,
            personalizacoes=item_data.personalizacoes,
        )
        db.add(item)
    
    db.commit()
    db.refresh(pedido)
    
    # Retornar resposta
    itens_response = []
    for item in pedido.itens:
        receita = db.query(Receita).filter(Receita.id == item.receita_id).first()
        itens_response.append(
            ItemPedidoResponse(
                id=item.id,
                receita_id=item.receita_id,
                quantidade=item.quantidade,
                unidade=item.unidade,
                personalizacoes=item.personalizacoes,
                receita_nome=receita.nome if receita else None,
            )
        )
    
    return PedidoResponse(
        id=pedido.id,
        cliente=pedido.cliente,
        status=pedido.status,
        data_entrega=pedido.data_entrega,
        horario=pedido.horario,
        local=pedido.local,
        observacoes=pedido.observacoes,
        preco_total=pedido.preco_total,
        itens=itens_response,
    )


@router.patch("/{pedido_id}", response_model=PedidoResponse)
def atualizar_pedido(
    pedido_id: int, pedido_data: PedidoUpdate, db: Session = Depends(get_db)
):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    update_data = pedido_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(pedido, field, value)
    
    db.commit()
    db.refresh(pedido)
    
    itens_response = []
    for item in pedido.itens:
        receita = db.query(Receita).filter(Receita.id == item.receita_id).first()
        itens_response.append(
            ItemPedidoResponse(
                id=item.id,
                receita_id=item.receita_id,
                quantidade=item.quantidade,
                unidade=item.unidade,
                personalizacoes=item.personalizacoes,
                receita_nome=receita.nome if receita else None,
            )
        )
    
    return PedidoResponse(
        id=pedido.id,
        cliente=pedido.cliente,
        status=pedido.status,
        data_entrega=pedido.data_entrega,
        horario=pedido.horario,
        local=pedido.local,
        observacoes=pedido.observacoes,
        preco_total=pedido.preco_total,
        itens=itens_response,
    )


@router.patch("/{pedido_id}/status", response_model=PedidoResponse)
def atualizar_status_pedido(
    pedido_id: int, status_data: PedidoStatusUpdate, db: Session = Depends(get_db)
):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    pedido.status = status_data.status
    db.commit()
    db.refresh(pedido)
    
    itens_response = []
    for item in pedido.itens:
        receita = db.query(Receita).filter(Receita.id == item.receita_id).first()
        itens_response.append(
            ItemPedidoResponse(
                id=item.id,
                receita_id=item.receita_id,
                quantidade=item.quantidade,
                unidade=item.unidade,
                personalizacoes=item.personalizacoes,
                receita_nome=receita.nome if receita else None,
            )
        )
    
    return PedidoResponse(
        id=pedido.id,
        cliente=pedido.cliente,
        status=pedido.status,
        data_entrega=pedido.data_entrega,
        horario=pedido.horario,
        local=pedido.local,
        observacoes=pedido.observacoes,
        preco_total=pedido.preco_total,
        itens=itens_response,
    )

