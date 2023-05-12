from sqlalchemy.orm import Session
from lib.dao.models.user import User
from lib.dao.database import get_database

class UserRepository:
    @staticmethod
    def find_all(database: Session = get_database()) -> list[User]:
        '''Função para fazer uma query de todas as User da DB'''
        return database.query(User).all()
    
    @staticmethod
    def find_by_id(id: str, database: Session = get_database()) -> User:
        '''Função para fazer uma query com base no id (por enquanto desconsiderando o firebase_uid)'''
        return database.query(User).filter(User.firebase_uid == id).first()
    
    @staticmethod
    def create(firebase_uid, user: User, database: Session = get_database()) -> User:
        '''Função para criar um usuario'''
        user.firebase_uid = firebase_uid
        database.add(user)
        database.commit()
        return user

    @staticmethod
    def update(user: User, database: Session = get_database()) -> User:
        '''Função para salvar um objeto aluna na DB'''
        database.merge(user)
        database.commit()
        return user
