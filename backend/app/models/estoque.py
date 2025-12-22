from sqlalchemy import Column, Integer, ForeignKey, Numeric, Date, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum
from datetime import date


class TipoMovimentacao(str, enum.Enum):
    ENTRADA = "entrada"
    SAIDA = "saida"
    AJUSTE = "ajuste"


class Estoque(Base):
    __tablename__ = "estoque"

    ingrediente_id = Column(Integer, ForeignKey("ingredientes.id"), primary_key=True)
    quantidade_atual = Column(Numeric(10, 2), nullable=False, default=0)
    custo_unitario = Column(Numeric(10, 2))
    ponto_reposicao = Column(Numeric(10, 2), default=0)
    
    ingrediente = relationship("Ingrediente")


class MovimentacaoEstoque(Base):
    __tablename__ = "movimentacoes_estoque"

    id = Column(Integer, primary_key=True, index=True)
    ingrediente_id = Column(Integer, ForeignKey("ingredientes.id"), nullable=False, index=True)
    tipo = Column(SQLEnum(TipoMovimentacao), nullable=False)
    quantidade = Column(Numeric(10, 2), nullable=False)
    motivo = Column(String)  # produção, compra, ajuste, etc.
    data = Column(Date, nullable=False, default=date.today, index=True)
    
    ingrediente = relationship("Ingrediente")

