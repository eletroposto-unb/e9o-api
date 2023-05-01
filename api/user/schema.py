from pydantic import BaseModel

class UserBase(BaseModel):
    '''Classe para definir os modelos recebidos na API'''
    name: str


class UserRequest(UserBase):
    '''...'''

class UserResponse(UserBase):
    '''Classe para definir o Usuário devolvido pela API'''
    id: int
    class Config:
        orm_mode = True