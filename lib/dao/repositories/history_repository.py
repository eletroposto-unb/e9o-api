from typing import List
from sqlalchemy.orm import Session
from lib.dao.models.history import History

class HistoryRepository:
    @staticmethod
    def create(database: Session ,history: History) -> History:
        '''Função para criar um Carro'''
        try:
            database.add(history)
            database.commit()
        except:
            database.rollback()
        return history
    
    @staticmethod
    def find_all_by_cpf(cpf, database: Session) -> object:
        '''Função para fazer uma query de todos os Carros do DB'''
        histories = database.query(History).filter(cpf == History.cpf).all()

        res = {
            "user_history": histories
        }
        return res
