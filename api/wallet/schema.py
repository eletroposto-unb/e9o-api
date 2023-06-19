from pydantic import BaseModel

class WalletBase(BaseModel):
    '''Classe para definir os modelos recebidos na API'''
    qtdCreditos: int
    qtdCreditosSolicitados: int


class WalletRequest(WalletBase):
    '''...'''


class WalletResponse(WalletBase):
    '''Classe para definir a carteira devolvida pela API'''
    idCarteira: int
    cpf: str 
    class Config:
        orm_mode = True