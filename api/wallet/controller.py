from fastapi import APIRouter, Depends, status
from api.wallet.schema import WalletRequest, WalletResponse

from lib.dao.database import get_database
from lib.dao.repositories.wallet_repository import WalletRepository
from lib.dao.models.wallet import Wallet
from sqlalchemy.orm import Session

wallets = APIRouter(
    prefix = '/wallet',
    tags = ['wallets'],
    responses = {404: {"description": "Not found"}},
)

@wallets.post(
    "/register/",
    status_code = status.HTTP_201_CREATED,
    response_model=WalletResponse
)
def create_wallet(
  request: WalletRequest,
  database: Session = Depends(get_database)
):
  '''Cria carteira para usuario'''
  res = WalletRepository.create(Wallet(**request.dict()), database=database)
  return WalletResponse.from_orm(res)

@wallets.get(
    "/credits/{cpf}",
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

@wallets.delete(
    "/{id}",
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