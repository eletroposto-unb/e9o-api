from typing import List
from sqlalchemy.orm import Session
from lib.dao.models.history import History
from lib.dao.models.station import Station
from lib.dao.models.user import User

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
        histories = database.query(History)
        for history in histories:
            posto = database.query(Station).filter(Station.idPosto == history.idPosto).first()
            usuario = database.query(User).filter(User.cpf == history.cpf).first()
            history.posto = posto
            history.usuario = usuario

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
            history.posto = posto

        res = {
            "user_history": histories
        }
        return res

    @staticmethod
    def find_by_station_id(idPosto, database: Session) -> object:
        '''Função para fazer uma query de todos os historicos de um posto do DB'''
        histories = database.query(History).filter(idPosto == History.idPosto).all()
        for history in histories:
            posto = database.query(Station).filter(Station.idPosto == history.idPosto).first().nome
            usuario = database.query(User).filter(User.cpf == history.cpf).first()
            history.posto = posto
            history.usuario = usuario

        res = {
            "station_history": histories
        }
        return res