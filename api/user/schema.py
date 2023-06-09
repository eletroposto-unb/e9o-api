from pydantic import BaseModel
from api.wallet.schema import WalletBase

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

class UserWalletResponse(UserBase):
    '''Classe para definir o Usuário devolvido pela API'''
    firebase_uid: str
    wallet: object
    class Config:
        orm_mode = True