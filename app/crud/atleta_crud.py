from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.atleta import Atleta
from app.schemas.atleta_schema import AtletaCreate
from typing import List

async def criar_atletas(db: AsyncSession, atletas: List[AtletaCreate]):
    novos = [Atleta(nome=a.nome, cpf=a.cpf) for a in atletas]
    db.add_all(novos)
    await db.commit()
    for atleta in novos:
        await db.refresh(atleta)
    return novos

async def listar_atletas(db: AsyncSession):
    result = await db.execute(select(Atleta))
    return result.scalars().all()
