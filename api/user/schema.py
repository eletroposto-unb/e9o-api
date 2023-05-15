from pydantic import BaseModel

from enum import Enum

class statusEnum(str, Enum):
    INACTIVE = 'inactive'
    ACTIVE = 'active'

class UserBase(BaseModel):
    '''Classe para definir os modelos recebidos na API'''
    name: str
    surname: str
    email: str
    cpf: str
    is_admin: bool
    telefone: str
    status: statusEnum = statusEnum.ACTIVE


class UserRequest(UserBase):
    '''...'''

class UserResponse(UserBase):
    firebase_uid: str
    '''Classe para definir o Usuário devolvido pela API'''
    class Config:
        orm_mode = True