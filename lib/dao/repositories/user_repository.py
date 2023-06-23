from typing import List
from sqlalchemy.orm import Session
from lib.dao.models.user import User
from lib.dao.models.wallet import Wallet

class UserRepository:
    @staticmethod
    def find_all(database: Session) -> List[User]:
        '''Função para fazer uma query de todas as User da DB'''
        return database.query(User).all()
    
    @staticmethod
    def find_by_key(cpf, database: Session) -> User:
        '''Função para fazer uma query com base no cpf'''
        user = database.query(User).filter(User.cpf == cpf).first()
        user_wallet = database.query(Wallet).filter(Wallet.cpf == user.cpf).first()
        user.wallet = user_wallet
        return user

    @staticmethod
    def find_by_uid(firebase_uid, database: Session) -> User:
        '''Função para fazer uma query com base no uid'''
        user = database.query(User).filter(User.firebase_uid == firebase_uid).first()
        user_wallet = database.query(Wallet).filter(Wallet.cpf == user.cpf).first()
        user.wallet = user_wallet
        return user
    
    @staticmethod
    def create(firebase_uid, user: User, wallet: Wallet, database: Session) -> User:
        '''Função para criar um usuario'''
        try:
            user.firebase_uid = firebase_uid
            database.add(user)
            database.commit()

            wallet.cpf = user.cpf
            database.add(wallet)
            database.commit()
        except:
            database.rollback()

        database.refresh(wallet)

        user.wallet = wallet
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
