from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaResponse
from app.db.database import get_db
from app import schemas
from uuid import UUID 

router = APIRouter()


@router.get("/", response_model=list[CategoriaResponse])
async def listar_categorias(nome: str = Query(None), db: AsyncSession = Depends(get_db)):
    query = select(Categoria)
    if nome:
        query = query.where(Categoria.nome.ilike(f"%{nome}%"))
    result = await db.execute(query)
    categorias = result.scalars().all()
    return categorias


@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
async def criar_categoria(categoria: CategoriaCreate, db: AsyncSession = Depends(get_db)):
    nova_categoria = Categoria(
        nome=categoria.nome,
        descricao=categoria.descricao
    )
    db.add(nova_categoria)
    await db.commit()
    await db.refresh(nova_categoria)
    return nova_categoria



@router.put("/{categoria_id}", response_model=CategoriaResponse)
async def atualizar_categoria(
    categoria_id: UUID,
    categoria: CategoriaCreate,
    db: AsyncSession = Depends(get_db)
):
    query = select(Categoria).where(Categoria.id == categoria_id)
    result = await db.execute(query)
    db_categoria = result.scalars().first()

    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    db_categoria.nome = categoria.nome
    db_categoria.descricao = categoria.descricao
    await db.commit()
    await db.refresh(db_categoria)
    return db_categoria



@router.delete("/{categoria_id}", status_code=204)
async def deletar_categoria(
    categoria_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    query = select(Categoria).where(Categoria.id == categoria_id)
    result = await db.execute(query)
    db_categoria = result.scalars().first()

    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    await db.delete(db_categoria)
    await db.commit()
    return None  
