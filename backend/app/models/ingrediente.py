from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Ingrediente(Base):
    __tablename__ = "ingredientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True, index=True)
    unidade_padrao = Column(String, nullable=False)  # g, kg, ml, l, un

