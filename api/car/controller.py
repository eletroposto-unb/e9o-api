from typing import List
from fastapi import APIRouter, HTTPException, Request, status, Depends

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
def create(request: CarRequest, req: Request, db: Session = Depends(get_database)):
    
    if hasattr(req.state, 'exception'):
        return req.state.exception
    
    '''Cria e salva um carro'''
    car = CarRepository.create(db ,Car(**request.dict()))

    car.user_request = req.state.user
    print('usuario '+ car.user_request.name + ' requisitou')
    return car


@cars.get("/{id}",
    status_code = status.HTTP_200_OK,
    response_model=CarResponse
)
def find_one(id, req: Request, db: Session = Depends(get_database)):
    
    if hasattr(req.state, 'exception'):
        return req.state.exception
    
    '''Procura um carro pelo id'''
    car = CarRepository.find_by_key(id, db)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Carro não existe / não encontrado"
        )
    
    car.user_request = req.state.user
    print('usuario '+ car.user_request.name + ' requisitou')
    return CarResponse.from_orm(car)


@cars.get("/user/{cpf}",
    status_code = status.HTTP_200_OK,
)
def find_by_user(cpf: str, req: Request, db: Session = Depends(get_database)):

    if hasattr(req.state, 'exception'):
        return req.state.exception

    '''Procura todos os carros de um User pelo cpf'''
    cars = CarRepository.find_cars_by_user(cpf, db)
    if not cars:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Carros não existem / não encontrados"
        )
    # cars.user_request = req.state.user
    # print('usuario '+ cars.user_request.name + ' requisitou')
    return cars


@cars.get("/",
    status_code=status.HTTP_200_OK,
)
def find_all(req: Request,db: Session = Depends(get_database)):
    
    if hasattr(req.state, 'exception'):
        return req.state.exception

    '''Procura dodos os carros'''
    cars = CarRepository.find_all(db)

    # cars.user_request = req.state.user
    # print('usuario '+ cars.user_request.name + ' requisitou')
    return cars


@cars.put("/{id}",
    status_code = status.HTTP_200_OK,
    response_model=CarResponse
)
def update(id, req: Request, request: CarRequest,  db: Session = Depends(get_database)):
    
    if hasattr(req.state, 'exception'):
        return req.state.exception
    
    '''atualiza os dados do carro'''
    car = Car(**request.dict())
    car.id = id
    if not CarRepository.find_by_key(id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Carro não encontrado"
        )
    car = CarRepository.update(car, db)

    car.user_request = req.state.user
    print('usuario '+ car.user_request.name + ' requisitou')
    return car

@cars.delete("/car/{id}",
    status_code=status.HTTP_200_OK,
    response_model=CarResponse
)
def delete_by_id(id: int, req: Request, db: Session = Depends(get_database)):
    
    if hasattr(req.state, 'exception'):
        return req.state.exception

    '''Deleta o carro pelo id'''
    if not CarRepository.find_by_key(id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Carro não encontrado"
        )
    car = CarRepository.delete_by_id(id, db)
    
    car.user_request = req.state.user
    print('usuario '+ car.user_request.name + ' requisitou')
    return car