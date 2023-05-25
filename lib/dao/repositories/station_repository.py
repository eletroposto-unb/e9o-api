from typing import List
from sqlalchemy.orm import Session
from lib.dao.models.address import Address
from lib.dao.models.station import Station

class StationRepository:
    @staticmethod
    def create(station: Station, address: Address, database: Session) -> Station:
        '''Função para criar um posto'''
        exists_address = database.query(Address).filter_by(cep=address.cep).first() is not None

        if(exists_address == False):
            database.add(address)
            database.commit()
            database.refresh(address)

        address = database.query(Address).filter_by(cep=address.cep).first()
        idEndereco = address.idEndereco

        try:
            station.idEndereco = idEndereco
            database.add(station)
            database.commit()
            database.refresh(station)
        except:
            database.rollback()
        return station
    
    @staticmethod
    def find_all(database: Session) -> List[Station]:
        '''Função para fazer uma query de todas as Estacoes da DB'''
        return database.query(Station).all()
    
    @staticmethod
    def find_station_by_id(idStation, database: Session) -> Address:
        '''Função para fazer uma query de um endereco da DB'''
        return database.query(Station).filter(idStation==Station.idPosto).first()
    
    @staticmethod
    def find_address(idEndereco, database: Session) -> Address:
        '''Função para fazer uma query de um endereco da DB'''
        return database.query(Address).filter(idEndereco==Address.idEndereco).first()