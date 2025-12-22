from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, time
from decimal import Decimal
from app.models.pedido import StatusPedido


class ItemPedidoCreate(BaseModel):
    receita_id: int
    quantidade: int = 1
    unidade: Optional[str] = None
    personalizacoes: Optional[str] = None


class ItemPedidoResponse(BaseModel):
    id: int
    receita_id: int
    quantidade: int
    unidade: Optional[str]
    personalizacoes: Optional[str]
    receita_nome: Optional[str] = None

    class Config:
        from_attributes = True


class PedidoCreate(BaseModel):
    cliente: str
    data_entrega: date
    horario: Optional[time] = None
    local: Optional[str] = None
    observacoes: Optional[str] = None
    itens: List[ItemPedidoCreate]
    preco_total: Optional[Decimal] = None


class PedidoUpdate(BaseModel):
    cliente: Optional[str] = None
    status: Optional[StatusPedido] = None
    data_entrega: Optional[date] = None
    horario: Optional[time] = None
    local: Optional[str] = None
    observacoes: Optional[str] = None
    preco_total: Optional[Decimal] = None


class PedidoResponse(BaseModel):
    id: int
    cliente: str
    status: StatusPedido
    data_entrega: date
    horario: Optional[time]
    local: Optional[str]
    observacoes: Optional[str]
    preco_total: Optional[Decimal]
    itens: List[ItemPedidoResponse]

    class Config:
        from_attributes = True


class PedidoStatusUpdate(BaseModel):
    status: StatusPedido

