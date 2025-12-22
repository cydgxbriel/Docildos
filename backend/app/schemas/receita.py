from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal


class IngredienteReceitaCreate(BaseModel):
    ingrediente_id: int
    quantidade: Decimal
    unidade: str


class IngredienteReceitaResponse(BaseModel):
    id: int
    ingrediente_id: int
    quantidade: Decimal
    unidade: str
    ingrediente_nome: Optional[str] = None

    class Config:
        from_attributes = True


class ReceitaCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    tempo_preparo: Optional[int] = None
    rendimento: Optional[str] = None
    ingredientes: List[IngredienteReceitaCreate]


class ReceitaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    tempo_preparo: Optional[int] = None
    rendimento: Optional[str] = None
    ingredientes: Optional[List[IngredienteReceitaCreate]] = None


class ReceitaResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    tempo_preparo: Optional[int]
    rendimento: Optional[str]
    ingredientes: List[IngredienteReceitaResponse]

    class Config:
        from_attributes = True

