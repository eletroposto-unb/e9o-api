from fastapi import APIRouter, Depends, HTTPException, Request, status
from api.wallet.schema import WalletRequest, WalletResponse, WalletRequestCreditos, WalletRequestSolicita

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
    response_model=WalletResponse
)
def create_wallet(
  request: WalletRequest,
  req: Request,
  database: Session = Depends(get_database)
):
  
  if hasattr(req.state, 'exception'):
        return req.state.exception
  
  '''Cria carteira para usuario'''
  wallet = WalletRepository.create(Wallet(**request.dict()), database=database)

  wallet.user_request = req.state.user
  print('usuario '+ wallet.user_request.name + ' requisitou')
  return wallet


@wallets.get("/credits/{cpf}",
    status_code = status.HTTP_200_OK,
    response_model=WalletResponse
)
def show_credits(
  cpf: str,
  req: Request,
  database: Session = Depends(get_database)
):
  '''Visualiza total de moedas do usuário'''
  wallet = WalletRepository.find_user_credits(cpf, database=database) 

  if not wallet:
     raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não existe"
      )

  wallet.user_request = req.state.user
  print('usuario '+ wallet.user_request.name + ' requisitou')
  return wallet


@wallets.put("/creditos/{cfp}",
    status_code = status.HTTP_200_OK,
    response_model=WalletResponse
)
def update(
    cpf: str,
    request: WalletRequestCreditos,  
    req: Request,
    database: Session = Depends(get_database)
  ):
    
    if hasattr(req.state, 'exception'):
        return req.state.exception
    
    '''atualiza os dados do total de creditos'''
    old_wallet = WalletRepository.find_user_credits(cpf, database=database)

    if(not old_wallet):
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não existe"
      )
    else:
      new_wallet = Wallet(**request.dict())
      old_wallet.qtdCreditos = new_wallet.qtdCreditos
      wallet = WalletRepository.update(old_wallet, database)

      wallet.user_request = req.state.user
      print('usuario '+ wallet.user_request.name + ' requisitou')
      return wallet
    

@wallets.put("/creditosSolicitados/{cfp}",
    status_code = status.HTTP_200_OK,
    response_model=WalletResponse
)
def update(
    cpf: str,
    request: WalletRequestSolicita,
    req: Request,
    database: Session = Depends(get_database)
  ):
    
    if hasattr(req.state, 'exception'):
        return req.state.exception
    
    '''atualiza os dados de creditos solicitados'''
    old_wallet = WalletRepository.find_user_credits(cpf, database=database)

    if(not old_wallet):
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não existe"
      )
    else:
      new_wallet = Wallet(**request.dict())
      old_wallet.qtdCreditosSolicitados = new_wallet.qtdCreditosSolicitados
      wallet = WalletRepository.update(old_wallet, database)

      wallet.user_request = req.state.user
      print('usuario '+ wallet.user_request.name + ' requisitou')
      return wallet


@wallets.delete("/{id}",
    status_code = status.HTTP_200_OK,
)
def delete_by_id(
  id: int,
  req: Request,
  database: Session = Depends(get_database)
):
  
  if hasattr(req.state, 'exception'):
        return req.state.exception
  
  '''Deleta carteira pelo id'''
  wallet = WalletRepository.delete_by_id(id, database=database)
  
  setattr(wallet, 'user_request', req.state.user)
  print('usuario '+ wallet.user_request.name + ' requisitou')
  return wallet