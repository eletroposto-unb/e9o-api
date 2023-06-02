from typing import List
from sqlalchemy.orm import Session
from lib.dao.models.address import Address
from lib.dao.models.station import Station

class StationRepository:
    @staticmethod
    def create(station: Station, address: Address, database: Session) -> Station:
        '''Função para criar um posto'''
        exists_address = database.query(Address).filter_by(cep=address.cep).first() is not None

        database.add(address)
        database.commit()
        database.refresh(address)

        print(address)
        # address = database.query(Address).filter_by(cep=address.cep).first()
        # idEndereco = address.idEndereco

        try:
            station.idEndereco = address.idEndereco
            database.add(station)
            database.commit()
            database.refresh(station)
        except:
            database.rollback()

        res = {
            'station': station,
            'address': address
        }

        print(res['address'].cep)

        return res
    
    @staticmethod
    def find_all(database: Session) -> List[Station]:
        '''Função para fazer uma query de todas as Estacoes da DB'''
        return database.query(Station).all()
    
    @staticmethod
    def find_station_by_id(idStation, database: Session) -> Address:
        '''Função para fazer uma query de um posto pelo id da DB'''
        return database.query(Station).filter(idStation==Station.idPosto).first()
    
    @staticmethod
    def find_address(idEndereco, database: Session) -> Address:
        '''Função para fazer uma query de um endereco da DB'''
        return database.query(Address).filter(idEndereco==Address.idEndereco).first()
    
    @staticmethod
    def update_station(idPosto, station: Station, address: Address, database: Session) -> Station:
        exists_address = database.query(Address).filter_by(cep=address.cep).first() is not None

        if(exists_address == False):
            database.add(address)
            database.commit()
            database.refresh(address)

        address = database.query(Address).filter_by(cep=address.cep).first()
        idEndereco = address.idEndereco

        try:
            station.idEndereco = idEndereco
            station.idPosto = idPosto
            database.merge(station)
            database.commit()
            database.refresh(station)
        except:
            database.rollback()
        print(station.idPosto)
        return station
    
    @staticmethod
    def delete_by_id(idStation: int, database: Session,) -> Station:
        station = database.query(Station).filter(Station.idPosto == idStation).first()
        if station is not None:
            database.delete(station)
            database.commit()
            return station