from typing import List
from sqlalchemy.orm import Session
from lib.dao.models.wallet import Wallet

class WalletRepository:
    @staticmethod
    def find_all(database: Session) -> List[Wallet]:
        '''Função para fazer uma query de todos as carteiras do DB'''
        return database.query(Wallet).all()
    
    @staticmethod
    def find_user_credits(cpf: str, database: Session) -> Wallet:
        '''Função para fazer uma query das carteiras com base no cpf do user'''
        return database.query(Wallet).filter(Wallet.cpf == cpf).first()

    @staticmethod
    def create(wallet: Wallet, database: Session) -> Wallet:
        '''Função para criar uma Carteira'''
        print(wallet)
        try:
            database.add(wallet)
            database.commit()
        except:
            database.rollback()
        return wallet

    @staticmethod
    def update(wallet: Wallet, database: Session) -> Wallet:
        '''Função para atualizar um objeto na DB'''
        try:
            database.merge(wallet)
            database.commit()
        except:
            database.rollback()
        return wallet
    
    @staticmethod
    def delete_by_id(idCarteira: int, database: Session) -> Wallet:
        wallet = database.query(Wallet).filter(Wallet.idCarteira == idCarteira).first()
        if wallet is not None:
            database.delete(wallet)
            database.commit()
            return wallet
