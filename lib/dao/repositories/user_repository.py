from typing import List
from sqlalchemy.orm import Session
from lib.dao.models.user import User

class UserRepository:
    @staticmethod
    def find_all(database: Session) -> List[User]:
        '''Função para fazer uma query de todas as User da DB'''
        return database.query(User).all()
    
    @staticmethod
    def find_by_key(cpf, database: Session) -> User:
        '''Função para fazer uma query com base no cpf'''
        return database.query(User).filter(User.cpf == cpf).first()

    @staticmethod
    def find_by_uid(firebase_uid, database: Session) -> User:
        '''Função para fazer uma query com base no cpf'''
        return database.query(User).filter(User.firebase_uid == firebase_uid).first()
    
    @staticmethod
    def create(firebase_uid, user: User, database: Session) -> User:
        '''Função para criar um usuario'''
        try:
            user.firebase_uid = firebase_uid
            database.add(user)
            database.commit()
        except:
            database.rollback()
        return user

    @staticmethod
    def update(firebase_uid: str ,user: User, database: Session) -> User:
        '''Função para atualizar um objeto na DB'''
        try:
            if user.cpf:
                user.firebase_uid = firebase_uid
                database.merge(user)
                database.commit()
        except:
            database.rollback()
        return user
    
    @staticmethod
    def update_status(user: User, database: Session) -> User:
        '''Função para atualizar um objeto na DB'''
        try:
            if user.cpf:
                database.merge(user)
                database.commit()
        except:
            database.rollback()
        return user
