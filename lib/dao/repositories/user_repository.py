from sqlalchemy.orm import Session
from lib.dao.models.user import User
from lib.dao.database import get_database

class UserRepository:
    @staticmethod
    def find_all(database: Session = get_database()) -> list[User]:
        '''Função para fazer uma query de todas as User da DB'''
        return database.query(User).all()
    
    @staticmethod
    def find_by_key(cpf, database: Session = get_database()) -> User:
        '''Função para fazer uma query com base no cpf'''
        return database.query(User).filter(User.cpf == cpf).first()

    @staticmethod
    def find_by_uid(firebase_uid, database: Session = get_database()) -> User:
        '''Função para fazer uma query com base no cpf'''
        return database.query(User).filter(User.firebase_uid == firebase_uid).first()
    
    @staticmethod
    def create(firebase_uid, user: User, database: Session = get_database()) -> User:
        '''Função para criar um usuario'''
        try:
            user.firebase_uid = firebase_uid
            database.add(user)
            database.commit()
        except:
            database.rollback()
        return user

    @staticmethod
    def update(user: User, database: Session = get_database()) -> User:
        '''Função para atualizar um objeto na DB'''
        try:
            database.merge(user)
            database.commit()
        except:
            database.rollback()
        return user
