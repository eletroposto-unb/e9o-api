from typing import List
from fastapi import APIRouter, HTTPException, status, Depends

from api.history.schema import CreateHistoryResponse, HistoryRequest
from lib.dao.models.history import History
from lib.dao.repositories.history_repository import HistoryRepository
from lib.dao.database import get_database
from sqlalchemy.orm import Session

history = APIRouter(
    prefix = '/history',
    tags = ['history'],
    responses = {404: {"description": "Not found"}},
)


@history.post("/register/",
    status_code = status.HTTP_201_CREATED,
    response_model=CreateHistoryResponse
)
def create(request: HistoryRequest, db: Session = Depends(get_database)):
    '''Cria e salva historico'''
    history = HistoryRepository.create(db ,History(**request.dict()))

    return history


@history.get("/",
    status_code = status.HTTP_200_OK,
)
def find_all(db: Session = Depends(get_database)):
    '''Busca todos os historicos'''
    res = HistoryRepository.find_all(db)

    return res


@history.get("/user/{cpf}",
    status_code = status.HTTP_200_OK,
)
def find_by_cpf(cpf: str, db: Session = Depends(get_database)):
    '''Busca historicos por cpf do usuario'''
    res = HistoryRepository.find_all_by_cpf(cpf, db)

    return res


@history.get("/station/{idPosto}",
    status_code = status.HTTP_200_OK,
)
def find_by_station_id(idPosto: str, db: Session = Depends(get_database)):
    '''Busca historicos por id do posto'''
    res = HistoryRepository.find_by_station_id(idPosto, db)

    return res