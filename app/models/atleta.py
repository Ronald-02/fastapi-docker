from sqlalchemy import Column, Integer, String, UniqueConstraint
from app.db.database import Base

class Atleta(Base):
    __tablename__ = "atletas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cpf = Column(String, unique=True, index=True)  # <- CPF único
    idade = Column(Integer)
    modalidade = Column(String)
    centro_treinamento = Column(String)
    categoria = Column(String)