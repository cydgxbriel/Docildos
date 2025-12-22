from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class AgendaEntrega(Base):
    __tablename__ = "agenda_entregas"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False, unique=True, index=True)
    data_hora = Column(DateTime, nullable=False, index=True)
    local = Column(String)
    responsavel = Column(String)
    
    pedido = relationship("Pedido", back_populates="agenda")

