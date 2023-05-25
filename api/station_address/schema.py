from pydantic import BaseModel

from enum import Enum

class statusEnum(str, Enum):
    INACTIVE = 'inactive'
    ACTIVE = 'active'

class StationBase(BaseModel):
    '''Classe para definir os modelos recebidos na API'''
    nome: str
    statusFuncionamento: statusEnum = statusEnum.ACTIVE
    precoKwh: float 
    horarioFuncionamento: str
    tipoTomada: str
    potencia: float

class AddressBase(BaseModel):
    cep: str
    latitude: float
    longitude: float
    estado: str
    cidade: str
    endereco: str
    complemento: str


class StationRequest(StationBase, AddressBase):
    '''Classe que define o que deve ser incluido dentro do request alem do Base'''

class StationResponse(StationBase):
    '''Classe para definir posto devolvido pela API'''
    idPosto: int 
    idEndereco: int
    class Config:
        orm_mode = True

class AddressResponse(AddressBase):
    '''Classe para definir endereco devolvido pela API'''
    idEndereco: int
    class Config:
        orm_mode = True
