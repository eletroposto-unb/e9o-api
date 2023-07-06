import datetime
from typing import List
from sqlalchemy.orm import Session
from lib.dao.models.history import History
from lib.dao.models.station import Station
from lib.dao.models.user import User
from lib.dao.models.car import Car

class HistoryRepository:
    @staticmethod
    def create(database: Session, history: History) -> History:
        '''Função para criar um historico'''
        try:
            database.add(history)
            database.commit()
        except:
            database.rollback()
        return history
    
    @staticmethod
    def find_all(database: Session) -> object:
        '''Função para fazer uma query de todos os historicos do DB'''
        histories = database.query(History).all()
        for history in histories:
            posto = database.query(Station).filter(Station.idPosto == history.idPosto).first()
            usuario = database.query(User).filter(User.cpf == history.cpf).first()
            carro = database.query(Car).filter(Car.id == history.idCarro).first()
            history.posto = posto
            history.usuario = usuario
            history.carro = carro

        res = {
            "history": histories
        }
        return res
    
    @staticmethod
    def find_all_by_cpf(cpf, database: Session) -> object:
        '''Função para fazer uma query de todos os historicos de um usuario do DB'''
        histories = database.query(History).filter(cpf == History.cpf).all()
        for history in histories:
            posto = database.query(Station).filter(Station.idPosto == history.idPosto).first()
            usuario = database.query(User).filter(User.cpf == history.cpf).first()
            carro = database.query(Car).filter(Car.id == history.idCarro).first()
            history.posto = posto
            history.carro = carro
            history.usuario = usuario

        res = {
            "history": histories
        }
        return res

    @staticmethod
    def find_last_by_id_station(database: Session, id_station: str, start_time: datetime.datetime):
        response = database.query(History).filter(id_station == History.idPosto).filter(start_time == History.horarioEntrada).first()
        return response
    
    def update(database: Session, history: History):
        response = database.merge(history)
        return response