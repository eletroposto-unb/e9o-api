from sqlalchemy import Column, Float, Integer, Sequence, String
from lib.dao.database import Base

class Address(Base):
    __tablename__ = 'addresses'

    idEndereco: int = Column(Integer, Sequence('seq_adress_table'), primary_key=True, index=True)
    cep: str = Column(String(9), nullable=False)
    comodidade: str = Column(String(100), nullable=False)
    latitude: float =  Column(Float, nullable=False)
    longitude: float = Column(Float, nullable=False)
    estado: str = Column(String(100), nullable=False)
    cidade: str = Column(String(100), nullable=False)
    endereco: str = Column(String(100), nullable=False)
    numero: int = Column(Integer, nullable=False)
    complemento: str = Column(String(100))

    