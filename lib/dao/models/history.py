from sqlalchemy import Column, Float, ForeignKey, Integer, Sequence, String
from lib.dao.database import Base
from lib.dao.models.car import Car
from lib.dao.models.station import Station
from lib.dao.models.user import User
from lib.dao.utc import utcnow

from sqlalchemy.types import DateTime

class History(Base):
    __tablename__ = 'histories'

    id: int = Column(Integer, Sequence('seq_history_table'), primary_key=True, index=True)
    horarioEntrada = Column(DateTime)
    horarioSaida = Column(DateTime)
    valorTotal: float = Column(Float, nullable=False)

    idPosto: int = Column(Integer, ForeignKey(Station.idPosto), nullable=False)
    cpf: str = Column(String(100), ForeignKey(User.cpf), nullable=False)
    idCarro: int = Column(Integer, ForeignKey(Car.id), nullable=False)