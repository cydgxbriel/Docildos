from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from decimal import Decimal
from app.db.database import get_db
from app.models.estoque import Estoque, MovimentacaoEstoque, TipoMovimentacao
from app.models.ingrediente import Ingrediente
from app.schemas.estoque import (
    EstoqueResponse,
    MovimentacaoEstoqueCreate,
    MovimentacaoEstoqueResponse,
)

router = APIRouter(prefix="/api/estoque", tags=["estoque"])


@router.get("", response_model=List[EstoqueResponse])
def listar_estoque(
    ingrediente_id: Optional[int] = Query(None),
    baixo_estoque: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Estoque)
    
    if ingrediente_id:
        query = query.filter(Estoque.ingrediente_id == ingrediente_id)
    
    estoques = query.all()
    
    result = []
    for estoque in estoques:
        ingrediente = (
            db.query(Ingrediente)
            .filter(Ingrediente.id == estoque.ingrediente_id)
            .first()
        )
        
        # Filtrar baixo estoque se solicitado
        if baixo_estoque and estoque.quantidade_atual >= estoque.ponto_reposicao:
            continue
        
        result.append(
            EstoqueResponse(
                ingrediente_id=estoque.ingrediente_id,
                ingrediente_nome=ingrediente.nome if ingrediente else None,
                quantidade_atual=estoque.quantidade_atual,
                custo_unitario=estoque.custo_unitario,
                ponto_reposicao=estoque.ponto_reposicao or Decimal("0"),
                unidade_padrao=ingrediente.unidade_padrao if ingrediente else None,
            )
        )
    return result


@router.get("/{ingrediente_id}", response_model=EstoqueResponse)
def obter_estoque(ingrediente_id: int, db: Session = Depends(get_db)):
    estoque = (
        db.query(Estoque).filter(Estoque.ingrediente_id == ingrediente_id).first()
    )
    if not estoque:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    
    ingrediente = (
        db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
    )
    
    return EstoqueResponse(
        ingrediente_id=estoque.ingrediente_id,
        ingrediente_nome=ingrediente.nome if ingrediente else None,
        quantidade_atual=estoque.quantidade_atual,
        custo_unitario=estoque.custo_unitario,
        ponto_reposicao=estoque.ponto_reposicao or Decimal("0"),
        unidade_padrao=ingrediente.unidade_padrao if ingrediente else None,
    )


@router.post("/movimentacao", response_model=MovimentacaoEstoqueResponse, status_code=201)
def registrar_movimentacao(
    movimentacao_data: MovimentacaoEstoqueCreate, db: Session = Depends(get_db)
):
    # Verificar se ingrediente existe
    ingrediente = (
        db.query(Ingrediente)
        .filter(Ingrediente.id == movimentacao_data.ingrediente_id)
        .first()
    )
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado")
    
    # Criar ou atualizar estoque
    estoque = (
        db.query(Estoque)
        .filter(Estoque.ingrediente_id == movimentacao_data.ingrediente_id)
        .first()
    )
    
    if not estoque:
        estoque = Estoque(
            ingrediente_id=movimentacao_data.ingrediente_id,
            quantidade_atual=Decimal("0"),
        )
        db.add(estoque)
    
    # Atualizar quantidade
    if movimentacao_data.tipo == TipoMovimentacao.ENTRADA:
        estoque.quantidade_atual += movimentacao_data.quantidade
    elif movimentacao_data.tipo == TipoMovimentacao.SAIDA:
        estoque.quantidade_atual -= movimentacao_data.quantidade
        if estoque.quantidade_atual < 0:
            estoque.quantidade_atual = Decimal("0")
    else:  # AJUSTE
        estoque.quantidade_atual = movimentacao_data.quantidade
    
    # Criar movimentação
    movimentacao = MovimentacaoEstoque(
        ingrediente_id=movimentacao_data.ingrediente_id,
        tipo=movimentacao_data.tipo,
        quantidade=movimentacao_data.quantidade,
        motivo=movimentacao_data.motivo,
        data=movimentacao_data.data or date.today(),
    )
    db.add(movimentacao)
    
    db.commit()
    db.refresh(movimentacao)
    
    return MovimentacaoEstoqueResponse(
        id=movimentacao.id,
        ingrediente_id=movimentacao.ingrediente_id,
        ingrediente_nome=ingrediente.nome,
        tipo=movimentacao.tipo,
        quantidade=movimentacao.quantidade,
        motivo=movimentacao.motivo,
        data=movimentacao.data,
    )


@router.get("/movimentacoes/historico", response_model=List[MovimentacaoEstoqueResponse])
def listar_movimentacoes(
    ingrediente_id: Optional[int] = Query(None),
    data_inicio: Optional[date] = Query(None),
    data_fim: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(MovimentacaoEstoque)
    
    if ingrediente_id:
        query = query.filter(MovimentacaoEstoque.ingrediente_id == ingrediente_id)
    if data_inicio:
        query = query.filter(MovimentacaoEstoque.data >= data_inicio)
    if data_fim:
        query = query.filter(MovimentacaoEstoque.data <= data_fim)
    
    movimentacoes = query.order_by(MovimentacaoEstoque.data.desc()).all()
    
    result = []
    for mov in movimentacoes:
        ingrediente = (
            db.query(Ingrediente)
            .filter(Ingrediente.id == mov.ingrediente_id)
            .first()
        )
        result.append(
            MovimentacaoEstoqueResponse(
                id=mov.id,
                ingrediente_id=mov.ingrediente_id,
                ingrediente_nome=ingrediente.nome if ingrediente else None,
                tipo=mov.tipo,
                quantidade=mov.quantidade,
                motivo=mov.motivo,
                data=mov.data,
            )
        )
    return result

