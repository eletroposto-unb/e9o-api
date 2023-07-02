from ast import List
from pydantic import BaseModel

from sqlalchemy.types import DateTime
from sqlalchemy import types
from datetime import datetime

from lib.dao.models.history import History

class HistoryBase(BaseModel):
  '''Classe para definir os modelos recebidos na API'''
  horarioEntrada: datetime
  horarioSaida: datetime
  valorTotal: float
  idPosto: int 
  cpf: str 

class HistoryRequest(HistoryBase):
  '''...'''

class CreateHistoryResponse(HistoryBase):
  class Config:
    orm_mode = True


# class HistoryUserResponse():
#   '''Classe para definir o historico devolvido pela API'''
#   history: List[HistoryBase]
#   user: object
#   class Config:
#     orm_mode = True

# class HistoryStationResponse():
#   '''Classe para definir o historico devolvido pela API'''
#   history: List[HistoryBase]
#   user: List[object]
#   class Config:
#     orm_mode = True