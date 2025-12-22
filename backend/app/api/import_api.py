from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import csv
import io
from decimal import Decimal
from app.db.database import get_db
from app.models.ingrediente import Ingrediente
from app.models.estoque import Estoque

router = APIRouter(prefix="/api/import", tags=["import"])


@router.post("/custos")
async def importar_custos(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    """
    Importa CSV de custos no formato:
    ingrediente,custo_unitario,unidade
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Arquivo deve ser CSV")
    
    try:
        contents = await file.read()
        csv_content = contents.decode("utf-8")
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        
        linhas_processadas = 0
        erros = []
        
        for linha_num, row in enumerate(csv_reader, start=2):  # Começa em 2 (linha 1 é header)
            try:
                ingrediente_nome = row.get("ingrediente", "").strip()
                custo_str = row.get("custo_unitario", "").strip()
                unidade = row.get("unidade", "").strip()
                
                if not ingrediente_nome:
                    erros.append(f"Linha {linha_num}: Nome do ingrediente vazio")
                    continue
                
                try:
                    custo_unitario = Decimal(custo_str)
                except (ValueError, TypeError):
                    erros.append(
                        f"Linha {linha_num}: Custo inválido '{custo_str}'"
                    )
                    continue
                
                # Buscar ou criar ingrediente
                ingrediente = (
                    db.query(Ingrediente)
                    .filter(Ingrediente.nome.ilike(ingrediente_nome))
                    .first()
                )
                
                if not ingrediente:
                    # Criar ingrediente se não existir
                    ingrediente = Ingrediente(
                        nome=ingrediente_nome,
                        unidade_padrao=unidade or "g",
                    )
                    db.add(ingrediente)
                    db.flush()
                
                # Criar ou atualizar estoque
                estoque = (
                    db.query(Estoque)
                    .filter(Estoque.ingrediente_id == ingrediente.id)
                    .first()
                )
                
                if estoque:
                    estoque.custo_unitario = custo_unitario
                else:
                    estoque = Estoque(
                        ingrediente_id=ingrediente.id,
                        quantidade_atual=Decimal("0"),
                        custo_unitario=custo_unitario,
                        ponto_reposicao=Decimal("0"),
                    )
                    db.add(estoque)
                
                linhas_processadas += 1
                
            except Exception as e:
                erros.append(f"Linha {linha_num}: Erro ao processar - {str(e)}")
        
        db.commit()
        
        return {
            "message": "Importação concluída",
            "linhas_processadas": linhas_processadas,
            "erros": erros if erros else None,
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar arquivo: {str(e)}"
        )

