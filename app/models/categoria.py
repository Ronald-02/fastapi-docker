from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.database import Base

class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(UUID(as_uuid=True), default=lambda:str(uuid.uuid4()), primary_key= True)
    nome = Column(String, nullable=False)
    descricao = Column(String)