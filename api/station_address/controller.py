from typing import List
from fastapi import APIRouter, HTTPException, Request, status, Depends
from api.dependencies.verify_user import tokenToUser

from api.station_address.schema import ActiveStation, AddressResponse, StationObjectResponse, StationRequest, StationResponse
from lib.dao.models.address import Address
from lib.dao.models.station import Station
from lib.dao.repositories.station_repository import StationRepository
from lib.dao.repositories.wallet_repository import WalletRepository
from lib.dao.database import get_database

from datetime import datetime

from sqlalchemy.orm import Session

from lib.firestore.firestore import ChargeStatus, StationFields, set_firestore_field

stations = APIRouter(
    prefix = '/stations',
    tags = ['stations'],
    responses = {404: {"description": "Not found"}},
)

@stations.post("/register/",
    status_code = status.HTTP_201_CREATED
)
def create(
    request: StationRequest, 
    database: Session = Depends(get_database)
    ):
    '''Cria e salva um posto'''
    req = request.dict()

    station = {key: req[key] for key in req.keys()
              & {'nome', 'descricao', 'cabo','statusFuncionamento', 'precoKwh',
                'horarioFuncionamento', 'tipoTomada','potencia'}}
    
    address = {key: req[key] for key in req.keys()
              & {'cep', 'comodidade', 'latitude', 'longitude', 'estado',
                 'cidade', 'endereco', 'numero', 'complemento'}}
    
    res = StationRepository.create(Station(**station), Address(**address), database=database)

    return res

@stations.get("/",
            status_code = status.HTTP_200_OK,
            )
def find_all_stations(database: Session = Depends(get_database)):
    stations = StationRepository.find_all(database=database)
    return stations

@stations.get("/station/{idPosto}",
              status_code = status.HTTP_200_OK,
              )
def find_station_by_id(idPosto, database: Session = Depends(get_database)):
    res = StationRepository.find_station_by_id(idPosto=idPosto,database=database)
    return res

@stations.get("/station/address/{idEndereco}",
              status_code = status.HTTP_200_OK,
              response_model=AddressResponse
              )
def find_stations_address(idEndereco, database: Session = Depends(get_database)):
    address = StationRepository.find_address(idEndereco=idEndereco,database=database)
    return AddressResponse.from_orm(address)

@stations.put('/station/{idPosto}',
              status_code = status.HTTP_200_OK,
              )
def update_station(idPosto, request: StationRequest, database: Session = Depends(get_database)):
    '''atualiza os dados do posto'''
    old_station = StationRepository.find_station_by_id(idPosto=idPosto,database=database)

    if(not old_station):
       raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Posto não existe"
        )
    else:
        req = request.dict()

        new_station = {key: req[key] for key in req.keys()
              & {'nome', 'descricao', 'cabo','statusFuncionamento', 'precoKwh',
                'horarioFuncionamento', 'tipoTomada','potencia'}}
    
        new_address = {key: req[key] for key in req.keys()
              & {'cep', 'comodidade', 'latitude', 'longitude', 'estado',
                 'cidade', 'endereco', 'numero', 'complemento'}}
                 
        res = StationRepository.update_station(old_station,Station(**new_station), Address(**new_address), database=database)
        return res
    
@stations.delete('/station/{idPosto}',
                    status_code = status.HTTP_200_OK,
                    )
def delete_by_id(idPosto: int, database: Session = Depends(get_database)):
    if not StationRepository.find_station_by_id(idPosto, database):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Posto não encontrado"
        )
    res = StationRepository.delete_by_id(idPosto, database)
    return res

@stations.post("/activate/{idStation}",
    status_code = status.HTTP_200_OK
)
def activate_post(
    idStation: str,
    request: ActiveStation,
    database: Session = Depends(get_database),
    user: object = Depends(tokenToUser)
    ):
    
    if ChargeStatus.CHARGING == 0:
        wallet = WalletRepository.find_user_credits(user.cpf, database=database)
        station = StationRepository.find_station_by_id(idStation, database=database)
        wallet.qtdCreditos = wallet.qtdCreditos - (station['station'].precoKwh * request.charge_time / 60)
        if wallet.qtdCreditos < 0 :
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Creditos Insuficientes"
            )
        updated_wallet = WalletRepository.update(wallet,database=database)
        print(updated_wallet.qtdCreditos)

        '''Cria e salva um posto'''
        set_firestore_field(idStation, StationFields.charge, ChargeStatus.CHARGING)
        set_firestore_field(idStation, StationFields.charge_time, request.charge_time)
        set_firestore_field(idStation, StationFields.charge_start_time, datetime.now())
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Posto se encontra em uso"
        )
    user.wallet = updated_wallet
    print(user.wallet)
    return user