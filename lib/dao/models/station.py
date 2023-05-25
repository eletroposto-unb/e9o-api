from sqlalchemy import Column, Float, ForeignKey, Integer, Sequence, String
from lib.dao.database import Base
from lib.dao.models.address import Address

class Station(Base):
    __tablename__ = 'stations'

    idPosto: int = Column(Integer, Sequence('seq_station_table') ,primary_key=True, index=True)
    nome: str = Column(String(100), nullable=False)
    statusFuncionamento: str = Column(String(100), default='active')
    precoKwh: float = Column(Float)
    horarioFuncionamento: str = Column(String(100), nullable=False)
    tipoTomada: str = Column(String(100), nullable=False)
    potencia: int = Column(Integer, nullable=False)

    idEndereco: int = Column(Integer, ForeignKey(Address.idEndereco), nullable=False)
