from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from fastapi import Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.models import CentroTreinamento
from app.db.database import get_db
from typing import List
from app.schemas.centro_treinamento import CentroTreinamentoCreate,CentroTreinamentoResponse
from app import schemas 
from uuid import UUID 


router = APIRouter()


@router.get("/", response_model=list[CentroTreinamentoResponse])
async def listar_centros(nome: str = Query(None), db: AsyncSession = Depends(get_db)):
    query = select(CentroTreinamento)
    if nome:
        query = query.where(CentroTreinamento.nome.ilike(f"%{nome}%"))
    result = await db.execute(query)
    centros = result.scalars().all()
    return centros



@router.post("/", response_model=CentroTreinamentoResponse, status_code=201)
async def criar_centro_treinamento(
    centro: CentroTreinamentoCreate, db: AsyncSession = Depends(get_db)
):
    novo_centro = CentroTreinamento(
        nome=centro.nome,
        endereco=centro.endereco,
        proprietario=centro.proprietario,
    )
    db.add(novo_centro)
    try:
        await db.commit()
        await db.refresh(novo_centro)
        return novo_centro
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=303,
            detail=f"Centro de Treinamento com nome '{centro.nome}' já existe.",
        )


import traceback

@router.put("/{centro_id}", response_model=CentroTreinamentoResponse)
async def atualizar_centro(
    centro_id: UUID,
    centro: CentroTreinamentoCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(select(CentroTreinamento).where(CentroTreinamento.id == centro_id))
        db_centro = result.scalars().first()

        if not db_centro:
            raise HTTPException(status_code=404, detail="Centro de treinamento não encontrado")

        db_centro.nome = centro.nome
        db_centro.endereco = centro.endereco
        db_centro.proprietario = centro.proprietario

        await db.commit()
        await db.refresh(db_centro)
        return db_centro

    except Exception as e:
        print("Erro completo:")
        traceback.print_exc()  # Mostra o stack trace completo
        raise HTTPException(status_code=500, detail="Erro interno ao atualizar o centro")



@router.delete("/{centro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_centro(centro_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CentroTreinamento).where(CentroTreinamento.id == centro_id))
    db_centro = result.scalars().first()

    if not db_centro:
        raise HTTPException(status_code=404, detail="Centro de treinamento não encontrado")

    await db.delete(db_centro)
    await db.commit()
    return None
