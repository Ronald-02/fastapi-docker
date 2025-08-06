from pydantic import BaseModel
from typing import List
from uuid import UUID

class CategoriaBase(BaseModel):
    nome: str
    descricao: str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaOut(CategoriaBase):
    id: int

class CategoriaResponse(CategoriaBase):
    id: UUID
    nome: str
    descricao: str

    class Config:
        orm_mode = True

class CategoriaPayload(BaseModel):
    categorias: List[CategoriaBase]        