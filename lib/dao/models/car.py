from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer, String, Sequence
from lib.dao.models.user import User

from lib.dao.database import Base

class Car(Base):
    __tablename__ = 'cars'
    
    id: int = Column(Integer, Sequence('seq_car_table'), primary_key=True, index=True)
    placa: str = Column(String(100), nullable=False)
    modelo: str = Column(String(100), nullable=False)
    marca: str = Column(String(100), nullable=False)
    tipo: str = Column(String(100), nullable=False)
    ano: int = Column(Integer, nullable=False)
    tipoPlug: str = Column(String(100), nullable=False)
    cpf: str = Column(String(100), ForeignKey(User.cpf), nullable=False)

    
