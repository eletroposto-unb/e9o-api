from typing import Union
from pydantic import BaseModel

class UserBase(BaseModel):
    '''Classe para definir os modelos recebidos na API'''
    name: str


class UserRequest(UserBase):
    '''...'''