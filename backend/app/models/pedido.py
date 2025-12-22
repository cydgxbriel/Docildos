from sqlalchemy import Column, Integer, String, Date, Time, Text, Numeric, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum


class StatusPedido(str, enum.Enum):
    NOVO = "novo"
    EM_PRODUCAO = "em_producao"
    PRONTO = "pronto"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, nullable=False, index=True)
    status = Column(SQLEnum(StatusPedido), default=StatusPedido.NOVO, nullable=False, index=True)
    data_entrega = Column(Date, nullable=False, index=True)
    horario = Column(Time)
    local = Column(String)
    observacoes = Column(Text)
    preco_total = Column(Numeric(10, 2))
    
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")
    agenda = relationship("AgendaEntrega", back_populates="pedido", uselist=False, cascade="all, delete-orphan")


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    receita_id = Column(Integer, ForeignKey("receitas.id"), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)
    unidade = Column(String)  # g, kg, un - opcional para personalização
    personalizacoes = Column(Text)  # JSON string ou texto livre
    
    pedido = relationship("Pedido", back_populates="itens")
    receita = relationship("Receita")

