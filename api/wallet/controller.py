from fastapi import APIRouter, Depends, HTTPException, status
from api.wallet.schema import WalletRequest, WalletResponse, WalletRequestCreditos, WalletRequestSolicita, WalletRequestDevolve

from lib.dao.database import get_database
from lib.dao.repositories.wallet_repository import WalletRepository
from lib.dao.models.wallet import Wallet
from sqlalchemy.orm import Session

wallets = APIRouter(
    prefix = '/wallet',
    tags = ['wallets'],
    responses = {404: {"description": "Not found"}},
)

@wallets.post("/register/",
    status_code = status.HTTP_201_CREATED,
)
def create_wallet(
  request: WalletRequest,
  database: Session = Depends(get_database)
):
  '''Cria carteira para usuario'''
  res = WalletRepository.create(Wallet(**request.dict()), database=database)
  return res


@wallets.get("/credits/{cpf}",
    status_code = status.HTTP_200_OK,
    response_model=WalletResponse
)
def show_credits(
  cpf: str,
  database: Session = Depends(get_database)
):
  '''Visualiza total de moedas do usuário'''
  res = WalletRepository.find_user_credits(cpf, database=database) 
  return WalletResponse.from_orm(res)


@wallets.put("/aprovaCreditos/{cpf}",
    status_code = status.HTTP_200_OK,
    response_model=WalletResponse
)
def update(
    cpf: str,
    request: WalletRequestCreditos,  
    database: Session = Depends(get_database)
  ):
    '''atualiza os créditos da carteira'''
    old_wallet = WalletRepository.find_user_credits(cpf, database=database)

    requestBody = request.dict()
    if(not old_wallet):
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não existe"
      )
    elif(requestBody["aprovado"]):
      old_wallet.qtdCreditos = old_wallet.qtdCreditos + old_wallet.qtdCreditosSolicitados
      old_wallet.qtdCreditosSolicitados = 0
      wallet = WalletRepository.update(old_wallet, database)
      return WalletResponse.from_orm(wallet)
    else:
      old_wallet.qtdCreditosSolicitados = 0
      wallet = WalletRepository.update(old_wallet, database)
      return WalletResponse.from_orm(wallet)
      
      
    

@wallets.put("/creditosSolicitados/{cfp}",
    status_code = status.HTTP_200_OK,
    response_model=WalletResponse
)
def update(
    cpf: str,
    request: WalletRequestSolicita,  
    database: Session = Depends(get_database)
  ):
    '''atualiza os créditos solicitados'''
    old_wallet = WalletRepository.find_user_credits(cpf, database=database)

    if(not old_wallet):
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não existe"
      )
    else:
      new_wallet = Wallet(**request.dict())
      old_wallet.qtdCreditosSolicitados = new_wallet.qtdCreditosSolicitados
      wallet = WalletRepository.update(old_wallet, database)
      return WalletResponse.from_orm(wallet)


@wallets.put("/devolveCreditos/{cfp}",
    status_code = status.HTTP_200_OK,
    response_model=WalletResponse
)
def update(
    cpf: str,
    request: WalletRequestDevolve,  
    database: Session = Depends(get_database)
  ):
    '''atualiza os créditos solicitados'''
    old_wallet = WalletRepository.find_user_credits(cpf, database=database)

    if(not old_wallet):
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não existe"
      )
    else:
      new_wallet = Wallet(**request.dict())
      old_wallet.qtdCreditos = new_wallet.qtdCreditos + old_wallet.qtdCreditos
      wallet = WalletRepository.update(old_wallet, database)
      return WalletResponse.from_orm(wallet)

@wallets.delete("/{id}",
    status_code = status.HTTP_200_OK,
    response_model=WalletResponse
)
def delete_by_id(
  id: int,
  database: Session = Depends(get_database)
):
  '''Deleta carteira pelo id'''
  res = WalletRepository.delete_by_id(id, database=database) 
  return WalletResponse.from_orm(res)