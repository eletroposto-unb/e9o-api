from typing import List
from fastapi import APIRouter, HTTPException, status, Depends

from api.station_address.schema import AddressResponse, StationRequest, StationResponse
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
    status_code = status.HTTP_201_CREATED,
    response_model=StationResponse
)
def create(
    request: StationRequest, 
    database: Session = Depends(get_database)
    ):
    '''Cria e salva um posto'''
    req = request.dict()

    station = {key: req[key] for key in req.keys()
              & {'nome', 'statusFuncionamento', 'precoKwh',
                'horarioFuncionamento', 'tipoTomada','potencia'}}
    
    address = {key: req[key] for key in req.keys()
              & {'cep', 'latitude', 'longitude', 'estado',
                 'cidade', 'endereco', 'complemento'}}
    res = StationRepository.create(Station(**station), Address(**address), database=database)
    return StationResponse.from_orm(res)

@stations.get("/",
            status_code = status.HTTP_200_OK,
            response_model=List[StationResponse]
            )
def find_all_stations(
        database: Session = Depends(get_database),
    ):
    stations = StationRepository.find_all(database=database)
    return [StationResponse.from_orm(station) for station in stations]

@stations.get("/station/{idStation}",
              status_code = status.HTTP_200_OK,
              response_model=StationResponse
              )
def find_station_by_id(
        idStation,
        database: Session = Depends(get_database),
    ):
    station = StationRepository.find_station_by_id(idStation=idStation,database=database)
    return StationResponse.from_orm(station)

@stations.get("/station/address/{idEndereco}",
              status_code = status.HTTP_200_OK,
              response_model=AddressResponse
              )
def find_stations_address(
        idEndereco,
        database: Session = Depends(get_database),
    ):
    address = StationRepository.find_address(idEndereco=idEndereco,database=database)
    return AddressResponse.from_orm(address)

@stations.put('/station/{idStation}',
              status_code = status.HTTP_200_OK,
              response_model=StationResponse
              )
def update_station(
    idStation,
    request: StationRequest,
    database: Session = Depends(get_database)
    ):
    '''atualiza os dados do posto'''
    station = StationRepository.find_station_by_id(idStation=idStation,database=database)

    if(not station):
       raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Posto não existe"
        )
    else:
        req = request.dict()

        station = {key: req[key] for key in req.keys()
                & {'nome', 'statusFuncionamento', 'precoKwh',
                'horarioFuncionamento', 'tipoTomada','potencia'}}
    
        address = {key: req[key] for key in req.keys()
                & {'cep', 'latitude', 'longitude', 'estado',
                 'cidade', 'endereco', 'complemento'}}

        updated_station = StationRepository.update_station(idStation,Station(**station), Address(**address), database=database)
        return StationResponse.from_orm(updated_station)