from typing import List
from fastapi import APIRouter, HTTPException, status, Depends

from api.car.schema import CarRequest, CarResponse
from lib.dao.models.car import Car
from lib.dao.repositories.cars_repository import CarRepository
from lib.dao.database import get_database
from sqlalchemy.orm import Session

cars = APIRouter(
    prefix = '/cars',
    tags = ['cars'],
    responses = {404: {"description": "Not found"}},
)


@cars.post("/register/",
    status_code = status.HTTP_201_CREATED,
    response_model=CarResponse
)
def create(request: CarRequest, db: Session = Depends(get_database)):
    '''Cria e salva um carro'''
    car = CarRepository.create(db ,Car(**request.dict()))

    return CarResponse.from_orm(car)


@cars.get("/{id}",
    status_code = status.HTTP_200_OK,
    response_model=CarResponse
)
def find_one(id, db: Session = Depends(get_database)):
    '''Procura um carro pelo id'''
    car = CarRepository.find_by_key(id, db)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Carro não existe / não encontrado"
        )
    return CarResponse.from_orm(car)


@cars.get("/user/{cpf}",
    status_code = status.HTTP_200_OK,
    response_model=List[CarResponse]
)
def find_by_user(cpf, db: Session = Depends(get_database)):
    '''Procura todos os carros de um User pelo cpf'''
    cars = CarRepository.find_cars_by_user(cpf, db)
    if not cars:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Carros não existem / não encontrados"
        )
    return [CarResponse.from_orm(car) for car in cars]


@cars.get("/",
    status_code=status.HTTP_200_OK,
    response_model=List[CarResponse]
)
def find_all(db: Session = Depends(get_database)):
    cars = CarRepository.find_all(db)
    return [CarResponse.from_orm(car) for car in cars]


@cars.put("/{id}",
    status_code = status.HTTP_200_OK,
    response_model=CarResponse
)
def update(id, request: CarRequest,  db: Session = Depends(get_database)):
    '''atualiza os dados do carro'''
    car = Car(**request.dict())
    car.id = id
    car = CarRepository.update(car, db)
    return CarResponse.from_orm(car)

@cars.delete("/car/{id}",
    status_code=status.HTTP_200_OK,
    response_model=CarResponse
)
def delete_by_id(id: int, db: Session = Depends(get_database)):
    if not CarRepository.find_by_key(id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Carro não encontrado"
        )
    car = CarRepository.delete_by_id(id, db)
    return CarResponse.from_orm(car)