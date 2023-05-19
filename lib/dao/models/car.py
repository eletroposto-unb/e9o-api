from sqlalchemy import BigInteger, Boolean, Column, Integer, String, Sequence
from sqlalchemy.orm import relationship

from lib.dao.database import Base

class Car(Base):
    __tablename__ = 'cars'
    
    idCarro: int = Column(String(128), primary_key=True, nullable=False, index=True)
    placa: str = Column(String(100), nullable=False)
    modelo: str = Column(String(100), nullable=False)
    marca: str = Column(String(100), nullable=False)
    tipo: str = Column(String(100), nullable=False)
    ano: int = Column(Integer, nullable=False)
    tipoPlug: str = Column(String(100), nullable=False)
    cpf: str = Column(String(100), nullable=False, ForeignKey("users.cpf"))

    
