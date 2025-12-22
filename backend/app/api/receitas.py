from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.models.receita import Receita, IngredienteReceita
from app.models.ingrediente import Ingrediente
from app.schemas.receita import (
    ReceitaCreate,
    ReceitaUpdate,
    ReceitaResponse,
    IngredienteReceitaResponse,
)

router = APIRouter(prefix="/api/receitas", tags=["receitas"])


@router.get("", response_model=List[ReceitaResponse])
def listar_receitas(
    nome: Optional[str] = Query(None), db: Session = Depends(get_db)
):
    query = db.query(Receita)
    
    if nome:
        query = query.filter(Receita.nome.ilike(f"%{nome}%"))
    
    receitas = query.all()
    
    result = []
    for receita in receitas:
        ingredientes_response = []
        for ing_rec in receita.ingredientes:
            ingrediente = (
                db.query(Ingrediente)
                .filter(Ingrediente.id == ing_rec.ingrediente_id)
                .first()
            )
            ingredientes_response.append(
                IngredienteReceitaResponse(
                    id=ing_rec.id,
                    ingrediente_id=ing_rec.ingrediente_id,
                    quantidade=ing_rec.quantidade,
                    unidade=ing_rec.unidade,
                    ingrediente_nome=ingrediente.nome if ingrediente else None,
                )
            )
        result.append(
            ReceitaResponse(
                id=receita.id,
                nome=receita.nome,
                descricao=receita.descricao,
                tempo_preparo=receita.tempo_preparo,
                rendimento=receita.rendimento,
                ingredientes=ingredientes_response,
            )
        )
    return result


@router.get("/{receita_id}", response_model=ReceitaResponse)
def obter_receita(receita_id: int, db: Session = Depends(get_db)):
    receita = db.query(Receita).filter(Receita.id == receita_id).first()
    if not receita:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    
    ingredientes_response = []
    for ing_rec in receita.ingredientes:
        ingrediente = (
            db.query(Ingrediente)
            .filter(Ingrediente.id == ing_rec.ingrediente_id)
            .first()
        )
        ingredientes_response.append(
            IngredienteReceitaResponse(
                id=ing_rec.id,
                ingrediente_id=ing_rec.ingrediente_id,
                quantidade=ing_rec.quantidade,
                unidade=ing_rec.unidade,
                ingrediente_nome=ingrediente.nome if ingrediente else None,
            )
        )
    
    return ReceitaResponse(
        id=receita.id,
        nome=receita.nome,
        descricao=receita.descricao,
        tempo_preparo=receita.tempo_preparo,
        rendimento=receita.rendimento,
        ingredientes=ingredientes_response,
    )


@router.post("", response_model=ReceitaResponse, status_code=201)
def criar_receita(receita_data: ReceitaCreate, db: Session = Depends(get_db)):
    receita = Receita(
        nome=receita_data.nome,
        descricao=receita_data.descricao,
        tempo_preparo=receita_data.tempo_preparo,
        rendimento=receita_data.rendimento,
    )
    db.add(receita)
    db.flush()
    
    # Criar ingredientes da receita
    for ing_data in receita_data.ingredientes:
        ing_rec = IngredienteReceita(
            receita_id=receita.id,
            ingrediente_id=ing_data.ingrediente_id,
            quantidade=ing_data.quantidade,
            unidade=ing_data.unidade,
        )
        db.add(ing_rec)
    
    db.commit()
    db.refresh(receita)
    
    ingredientes_response = []
    for ing_rec in receita.ingredientes:
        ingrediente = (
            db.query(Ingrediente)
            .filter(Ingrediente.id == ing_rec.ingrediente_id)
            .first()
        )
        ingredientes_response.append(
            IngredienteReceitaResponse(
                id=ing_rec.id,
                ingrediente_id=ing_rec.ingrediente_id,
                quantidade=ing_rec.quantidade,
                unidade=ing_rec.unidade,
                ingrediente_nome=ingrediente.nome if ingrediente else None,
            )
        )
    
    return ReceitaResponse(
        id=receita.id,
        nome=receita.nome,
        descricao=receita.descricao,
        tempo_preparo=receita.tempo_preparo,
        rendimento=receita.rendimento,
        ingredientes=ingredientes_response,
    )


@router.patch("/{receita_id}", response_model=ReceitaResponse)
def atualizar_receita(
    receita_id: int, receita_data: ReceitaUpdate, db: Session = Depends(get_db)
):
    receita = db.query(Receita).filter(Receita.id == receita_id).first()
    if not receita:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    
    update_data = receita_data.model_dump(exclude_unset=True)
    
    # Atualizar ingredientes se fornecido
    if "ingredientes" in update_data:
        # Remover ingredientes antigos
        db.query(IngredienteReceita).filter(
            IngredienteReceita.receita_id == receita_id
        ).delete()
        
        # Adicionar novos ingredientes
        for ing_data in update_data.pop("ingredientes"):
            ing_rec = IngredienteReceita(
                receita_id=receita.id,
                ingrediente_id=ing_data.ingrediente_id,
                quantidade=ing_data.quantidade,
                unidade=ing_data.unidade,
            )
            db.add(ing_rec)
    
    # Atualizar outros campos
    for field, value in update_data.items():
        setattr(receita, field, value)
    
    db.commit()
    db.refresh(receita)
    
    ingredientes_response = []
    for ing_rec in receita.ingredientes:
        ingrediente = (
            db.query(Ingrediente)
            .filter(Ingrediente.id == ing_rec.ingrediente_id)
            .first()
        )
        ingredientes_response.append(
            IngredienteReceitaResponse(
                id=ing_rec.id,
                ingrediente_id=ing_rec.ingrediente_id,
                quantidade=ing_rec.quantidade,
                unidade=ing_rec.unidade,
                ingrediente_nome=ingrediente.nome if ingrediente else None,
            )
        )
    
    return ReceitaResponse(
        id=receita.id,
        nome=receita.nome,
        descricao=receita.descricao,
        tempo_preparo=receita.tempo_preparo,
        rendimento=receita.rendimento,
        ingredientes=ingredientes_response,
    )

