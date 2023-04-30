from sqlalchemy.orm import Session
from lib.dao.models import User
from lib.dao.database import get_database

class UserRepository:
    @staticmethod
    def find_all(database: Session = get_database()) -> list[User]:
        '''Função para fazer uma query de todas as User da DB'''
        return database.query(User).all()

    @staticmethod
    def save(user: User, database: Session = get_database()) -> User:
        '''Função para salvar um objeto aluna na DB'''
        if user.id:
            database.merge(user)
        else:
            database.add(user)
        database.commit()
        return user
