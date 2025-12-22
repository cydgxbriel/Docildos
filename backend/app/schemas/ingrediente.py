from pydantic import BaseModel


class IngredienteCreate(BaseModel):
    nome: str
    unidade_padrao: str


class IngredienteResponse(BaseModel):
    id: int
    nome: str
    unidade_padrao: str

    class Config:
        from_attributes = True

