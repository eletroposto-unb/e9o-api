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
