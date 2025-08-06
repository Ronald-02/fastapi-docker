from pydantic import BaseModel
from typing import List
from uuid import UUID

class CentroTreinamentoBase(BaseModel):
    nome: str
    endereco: str
    proprietario: str


class CentroTreinamentoResponse(CentroTreinamentoBase):
    id: UUID
    nome: str
    endereco: str
    proprietario: str

    class Config:
        orm_mode = True

    
class CentroTreinamentoCreate(BaseModel):
    nome: str
    endereco: str
    proprietario: str


class CentroTreinamentoOut(BaseModel):
    id: int

    class Config:
        from_attributes = True