from fastapi import APIRouter, HTTPException, status

from api.car.schema import CarRequest, CarResponse
from lib.dao.models.car import Car
from lib.dao.repositories.car_repository import CarRepository

cars = APIRouter(
    prefix = '/cars',
    tags = ['cars'],
    responses = {404: {"description": "Not found"}},
)


@cars.post("/register/",
    status_code = status.HTTP_201_CREATED,
    response_model=carResponse
)
def create(request: carRequest):
    '''Cria e salva um carro'''
    car = carRepository.create(car(**request.dict()))
    return car


@cars.get("/{idCarro}",
    status_code = status.HTTP_200_OK,
    response_model=carResponse
)
def find_one(idCarro):
    '''Procura um carro pelo idCarro'''
    car = carRepository.find_by_key(idCarro)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Carro não existe / não encontrado"
        )
    return carResponse.from_orm(car)


@cars.get("/{cpf}",
    status_code = status.HTTP_200_OK,
    response_model=carResponse
)
def find_by_user(cpf):
    '''Procura todos os carros de um User pelo cpf'''
    cars = carRepository.find_cars_by_user(cpf)
    if not cars:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Carros não existem / não encontrados"
        )
    return [carResponse.from_orm(car) for car in cars]


@cars.get("/",
    status_code=status.HTTP_200_OK,
    response_model=list[carResponse]
)
def find_all():
    cars = carRepository.find_all()
    return [carResponse.from_orm(car) for car in cars]


@cars.put("/{idCarro}",
    status_code = status.HTTP_200_OK,
    response_model=carResponse
)
def update(idCarro, request: carRequest):
    '''atualiza os dados do carro'''
    car = carRepository.find_by_key(idCarro)
    car = carRepository.update(car(**request.dict()))
    return carResponse.from_orm(car)