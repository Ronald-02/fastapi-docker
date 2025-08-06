from pydantic import BaseModel
from typing import List
from uuid import UUID

# 🔹 Schema público (resumo com nome e nomes dos relacionamentos)
class AtletaPublic(BaseModel):
    nome: str
    centro_treinamento: str
    categoria: str

    class Config:
        orm_mode = True


# 🔹 Schema de resposta com CPF incluído
class AtletaOut(BaseModel):
    nome: str
    cpf: str
    centro_treinamento: str
    categoria: str

    class Config:
        orm_mode = True

class CentroTreinamentoSchema(BaseModel):
    id: UUID
    nome: str

class CategoriaSchema(BaseModel):
    id: UUID
    nome: str


# 🔹 Schema para criação de atletas via input do usuário
class AtletaCreate(BaseModel):
    nome: str
    idade: int
    modalidade: str
    cpf: str
    centro_treinamento: CentroTreinamentoSchema# nome do centro (não ID)
    categoria: CategoriaSchema         # nome da categoria (não ID)


# 🔹 Payload para criação de múltiplos atletas de uma vez
class AtletasPayload(BaseModel):
    atletas: List[AtletaCreate]


class AtletaUpdate(BaseModel):
    nome: str
    idade: int
    modalidade: str
    centro_treinamento: str  # nome, não ID
    categoria: str 

# 🔹 Schema de resposta básico
class AtletaResponse(BaseModel):
    nome: str
    centro_treinamento: str
    categoria: str

    class Config:
        orm_mode = True
