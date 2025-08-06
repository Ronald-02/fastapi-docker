from fastapi import Query, Path
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from app.models.atleta import Atleta
from app.db.database import get_db
from app.models import CentroTreinamento, Categoria
from app.schemas.atleta_schema import AtletaResponse, AtletasPayload, AtletaCreate, AtletaUpdate
from app import schemas
from fastapi_pagination import Page, paginate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from starlette.status import HTTP_303_SEE_OTHER, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter()

@router.get("/", response_model=Page[AtletaResponse])
async def listar_atletas(
    db: AsyncSession = Depends(get_db),
    nome: str = None,
    cpf: str = None
):
    query = select(Atleta)

    # Filtros opcionais
    if nome:
        query = query.where(Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.where(Atleta.cpf == cpf)

    result = await db.execute(query)
    atletas = result.scalars().all()

    # Mapeia os dados apenas com os campos desejados (customização)
    resposta = [
        AtletaResponse(
            nome=a.nome,
            centro_treinamento=a.centro_treinamento,
            categoria=a.categoria
        ) for a in atletas
    ]

    return paginate(resposta)

@router.post("/", response_model=dict)
async def criar_atletas(payload: AtletasPayload, db: AsyncSession = Depends(get_db)):
    try:
        for atleta in payload.atletas:
            novo = Atleta(
                nome=atleta.nome,
                idade=atleta.idade,
                modalidade=atleta.modalidade,
                cpf=atleta.cpf,  # se ainda não tiver, adicione isso
                centro_treinamento=atleta.centro_treinamento,  # idem
                categoria=atleta.categoria  # idem
            )
            db.add(novo)
        await db.commit()
        return {"msg": "Atletas criados com sucesso"}

    except IntegrityError as e:
        await db.rollback()

        # Verifica se erro é por duplicidade de CPF
        if 'cpf' in str(e.orig).lower():
            cpf_duplicado = next(
                (atleta.cpf for atleta in payload.atletas if atleta.cpf), "desconhecido"
            )
            raise HTTPException(
                status_code=HTTP_303_SEE_OTHER,
                detail=f"Já existe um atleta cadastrado com o cpf: {cpf_duplicado}"
            )

        raise HTTPException(
            status_code=400,
            detail="Erro de integridade nos dados"
        )

@router.put("/{cpf}", response_model=AtletaResponse)
async def atualizar_atleta(
     atleta: AtletaCreate,  # agora vem antes
    cpf: str = Path(..., description="CPF do atleta"),
    db: AsyncSession = Depends(get_db)
):
    query = select(Atleta).where(Atleta.cpf == cpf)
    result = await db.execute(query)
    db_atleta = result.scalars().first()

    if not db_atleta:
        raise HTTPException(status_code=404, detail="Atleta não encontrado")

    db_atleta.nome = atleta.nome
    db_atleta.idade = atleta.idade
    db_atleta.modalidade = atleta.modalidade
    db_atleta.cpf = atleta.cpf
    db_atleta.centro_treinamento_id = atleta.centro_treinamento.id
    db_atleta.categoria_id = atleta.categoria.id

    await db.commit()
    await db.refresh(db_atleta)
    return db_atleta




@router.delete("/{cpf}", status_code=HTTP_204_NO_CONTENT)
async def deletar_atleta(
    cpf: str = Path(..., description="CPF do atleta a ser deletado"),
    db: AsyncSession = Depends(get_db)
):
    query = select(Atleta).where(Atleta.cpf == cpf)
    result = await db.execute(query)
    atleta = result.scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Atleta com CPF {cpf} não encontrado"
        )

    await db.delete(atleta)
    await db.commit()
