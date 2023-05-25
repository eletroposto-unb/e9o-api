from typing import List
from sqlalchemy.orm import Session
from lib.dao.models.car import Car

class CarRepository:
    @staticmethod
    def find_all(database: Session) -> List[Car]:
        '''Função para fazer uma query de todos os Carros do DB'''
        return database.query(Car).all()

    @staticmethod
    def find_cars_by_user(cpf: str, database: Session) -> List[Car]:
        '''Função para fazer uma query com base no cpf do user'''
        return database.query(Car).filter(Car.cpf == cpf).all()

    @staticmethod
    def find_by_key(id, database: Session) -> Car:
        '''Função para fazer uma query com base no id'''
        return database.query(Car).filter(Car.id == id).first()
    
    @staticmethod
    def create(database: Session ,car: Car) -> Car:
        '''Função para criar um Carro'''
        try:
            database.add(car)
            database.commit()
        except:
            database.rollback()
        print('esse e o carro')
        return car

    @staticmethod
    def update(car: Car, database: Session) -> Car:
        '''Função para atualizar um objeto na DB'''
        try:
            database.merge(car)
            database.commit()
        except:
            database.rollback()
        return car
    
    @staticmethod
    def delete_by_id(id: int, database: Session,) -> Car:
        car = database.query(Car).filter(Car.id == id).first()
        if car is not None:
            database.delete(car)
            database.commit()
            return car
