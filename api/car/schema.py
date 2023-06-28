from pydantic import BaseModel

from enum import Enum

class tipoPlugEnum(str, Enum):
    #confirmar tipos e adaptadores
    TIPO2 = 'tipo 2'

class CarBase(BaseModel):
    '''Classe para definir os modelos recebidos na API'''
    placa: str
    modelo: str
    marca: str
    tipo: str
    ano: int
    tipoPlug: tipoPlugEnum = tipoPlugEnum.TIPO2
    cpf: str


class CarRequest(CarBase):
    '''...'''

class CarResponse(CarBase):
    '''Classe para definir o Carro devolvido pela API'''
    id: int
    user_request: object
    class Config:
        orm_mode = True