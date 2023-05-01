from sqlalchemy.orm import Session
from lib.dao.models.user import User
from lib.dao.database import get_database

class UserRepository:
    @staticmethod
    def find_all(database: Session = get_database()) -> list[User]:
        '''Função para fazer uma query de todas as User da DB'''
        return database.query(User).all()
    
    @staticmethod
    def create(user: User, database: Session = get_database()) -> User:
        '''Função para criar um usuario'''
        database.add(user)
        database.commit()
        return user

    @staticmethod
    def update(user: User, database: Session = get_database()) -> User:
        '''Função para salvar um objeto aluna na DB'''
        database.merge(user)
        database.commit()
        return user
