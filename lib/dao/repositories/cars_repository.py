from typing import List
from sqlalchemy.orm import Session
from lib.dao.models.car import Car
from lib.dao.models.user import User
from lib.dao.database import get_database

class CarRepository:
    @staticmethod
    def find_all(database: Session = get_database()) -> List[Car]:
        '''Função para fazer uma query de todos os Carros do DB'''
        return database.query(Car).all()

    @staticmethod
    def find_cars_by_user(cpf, database: Session = get_database()) -> List[Car]:
        '''Função para fazer uma query com base no id'''
        return database.query(Car).filter(Car.cpf == cpf).all()

    @staticmethod
    def find_by_key(id, database: Session = get_database()) -> Car:
        '''Função para fazer uma query com base no id'''
        return database.query(Car).filter(Car.id == id).first()
    
    @staticmethod
    def create(car: Car, database: Session = get_database()) -> Car:
        '''Função para criar um Carro'''
        try:
            database.add(car)
            database.commit()
        except:
            database.rollback()
        print('esse e o carro')
        return car

    @staticmethod
    def update(car: Car, database: Session = get_database()) -> Car:
        '''Função para atualizar um objeto na DB'''
        try:
            database.merge(car)
            database.commit()
        except:
            database.rollback()
        return car