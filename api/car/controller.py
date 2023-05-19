from typing import List
from fastapi import APIRouter, HTTPException, status

from api.car.schema import CarRequest, CarResponse
from lib.dao.models.car import Car
from lib.dao.repositories.cars_repository import CarRepository

cars = APIRouter(
    prefix = '/cars',
    tags = ['cars'],
    responses = {404: {"description": "Not found"}},
)


@cars.post("/register/",
    status_code = status.HTTP_201_CREATED,
    response_model=CarResponse
)
def create(request: CarRequest):
    '''Cria e salva um carro'''
    car = CarRepository.create(Car(**request.dict()))

    print(car)

    return CarResponse.from_orm(car)


@cars.get("/{idCarro}",
    status_code = status.HTTP_200_OK,
    response_model=CarResponse
)
def find_one(idCarro):
    '''Procura um carro pelo idCarro'''
    car = CarRepository.find_by_key(idCarro)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Carro não existe / não encontrado"
        )
    return CarResponse.from_orm(car)


@cars.get("/{cpf}",
    status_code = status.HTTP_200_OK,
    response_model=CarResponse
)
def find_by_user(cpf):
    '''Procura todos os carros de um User pelo cpf'''
    cars = CarRepository.find_cars_by_user(cpf)
    if not cars:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Carros não existem / não encontrados"
        )
    return [CarResponse.from_orm(car) for car in cars]


@cars.get("/",
    status_code=status.HTTP_200_OK,
    response_model=List[CarResponse]
)
def find_all():
    cars = CarRepository.find_all()
    return [CarResponse.from_orm(car) for car in cars]


@cars.put("/{idCarro}",
    status_code = status.HTTP_200_OK,
    response_model=CarResponse
)
def update(idCarro, request: CarRequest):
    '''atualiza os dados do carro'''
    car = CarRepository.find_by_key(idCarro)
    car = CarRepository.update(car(**request.dict()))
    return CarResponse.from_orm(car)