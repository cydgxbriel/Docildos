from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class StatsResponse(BaseModel):
    pedidos_hoje: int
    pedidos_novos: int
    entregas_pendentes: int
    em_producao: int
    estoque_baixo: int
    total_pedidos_hoje: Optional[Decimal] = None

