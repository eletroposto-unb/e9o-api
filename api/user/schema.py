from typing import List
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
    '''Classe para definir o Usuário devolvido pela API'''
    firebase_uid: str
    class Config:
        orm_mode = True

class UserRequestResponse(UserBase):
    '''Classe para definir o Usuário devolvido pela API'''
    firebase_uid: str
    user_request: object
    class Config:
        orm_mode = True

class UserRequestListResponse():
    '''Classe para definir o Usuário devolvido pela API'''
    users: List[object]
    user_request: object
    class Config:
        orm_mode = True