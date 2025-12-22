from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AgendaEntregaCreate(BaseModel):
    pedido_id: int
    data_hora: datetime
    local: Optional[str] = None
    responsavel: Optional[str] = None


class AgendaEntregaUpdate(BaseModel):
    data_hora: Optional[datetime] = None
    local: Optional[str] = None
    responsavel: Optional[str] = None


class AgendaEntregaResponse(BaseModel):
    id: int
    pedido_id: int
    data_hora: datetime
    local: Optional[str]
    responsavel: Optional[str]
    pedido_cliente: Optional[str] = None

    class Config:
        from_attributes = True

