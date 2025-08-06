from sqlalchemy import Column, String
from app.db.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class CentroTreinamento(Base):
    __tablename__ = "centro_treinamento"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    nome = Column(String, nullable=False, unique=True)
    endereco = Column(String, nullable=True)
    proprietario = Column(String, nullable=True)
