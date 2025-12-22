from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.database import Base


class Receita(Base):
    __tablename__ = "receitas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    descricao = Column(Text)
    tempo_preparo = Column(Integer)  # minutos
    rendimento = Column(String)  # ex: "2 unidades", "500g"
    
    ingredientes = relationship("IngredienteReceita", back_populates="receita", cascade="all, delete-orphan")


class IngredienteReceita(Base):
    __tablename__ = "ingrediente_receita"

    id = Column(Integer, primary_key=True, index=True)
    receita_id = Column(Integer, ForeignKey("receitas.id"), nullable=False)
    ingrediente_id = Column(Integer, ForeignKey("ingredientes.id"), nullable=False)
    quantidade = Column(Numeric(10, 2), nullable=False)
    unidade = Column(String, nullable=False)  # g, kg, ml, l, un
    
    receita = relationship("Receita", back_populates="ingredientes")
    ingrediente = relationship("Ingrediente")

