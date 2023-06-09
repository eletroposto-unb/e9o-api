from pydantic import BaseModel

class WalletBase(BaseModel):
    '''...'''
    qtdCreditos: int
    qtdCreditosSolicitados: int


class WalletRequestCreditos(BaseModel):
    '''...'''
    aprovado: bool


class WalletRequestSolicita(BaseModel):
    '''...'''
    qtdCreditosSolicitados: int


class WalletRequest(WalletBase):
    '''...'''
    cpf: str 


class WalletResponse(WalletRequest):
    '''Classe para definir a carteira devolvida pela API'''
    idCarteira: int
    class Config:
        orm_mode = True