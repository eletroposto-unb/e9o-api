from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, Sequence, String
from lib.dao.database import Base
from lib.dao.models.address import Address

class Station(Base):
    __tablename__ = 'stations'

    idPosto: int = Column(Integer, Sequence('seq_station_table') ,primary_key=True, index=True)
    nome: str = Column(String(100), nullable=False)
    descricao: str = Column(String(500), nullable=False)
    cabo: bool = Column(Boolean, nullable=False)
    statusFuncionamento: str = Column(String(100), nullable=False)
    precoKwh: float = Column(Float, nullable=False)
    horarioFuncionamento: str = Column(String(100), nullable=False)
    tipoTomada: str = Column(String(100), nullable=False)
    potencia: float = Column(Float, nullable=False)

    idEndereco: int = Column(Integer, ForeignKey(Address.idEndereco), nullable=False)
