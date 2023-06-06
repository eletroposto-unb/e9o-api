from typing import List
from fastapi import APIRouter, HTTPException, status, Depends

from api.station_address.schema import AddressResponse, StationObjectResponse, StationRequest, StationResponse
from lib.dao.models.address import Address
from lib.dao.models.station import Station
from lib.dao.repositories.station_repository import StationRepository
from lib.dao.database import get_database

from sqlalchemy.orm import Session

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