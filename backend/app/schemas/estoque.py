from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import date
from app.models.estoque import TipoMovimentacao


class EstoqueResponse(BaseModel):
    ingrediente_id: int
    ingrediente_nome: Optional[str] = None
    quantidade_atual: Decimal
    custo_unitario: Optional[Decimal]
    ponto_reposicao: Decimal
    unidade_padrao: Optional[str] = None

    class Config:
        from_attributes = True


class MovimentacaoEstoqueCreate(BaseModel):
    ingrediente_id: int
    tipo: TipoMovimentacao
    quantidade: Decimal
    motivo: Optional[str] = None
    data: Optional[date] = None


class MovimentacaoEstoqueResponse(BaseModel):
    id: int
    ingrediente_id: int
    ingrediente_nome: Optional[str] = None
    tipo: TipoMovimentacao
    quantidade: Decimal
    motivo: Optional[str]
    data: date

    class Config:
        from_attributes = True

