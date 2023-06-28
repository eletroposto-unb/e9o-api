from typing import List
from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from lib.dao.models.address import Address
from lib.dao.models.station import Station

class StationRepository:
    @staticmethod
    def create(station: Station, address: Address, req_user: object , database: Session) -> Station:
        '''Função para criar um posto'''
        try:
            database.add(address)
            database.commit()
            station.idEndereco = address.idEndereco
            database.add(station)
            database.commit()
            database.refresh(address)
            database.refresh(station)
        except:
            database.rollback()
            
        print(req_user.name)
        res = {
            'station': station,
            'address': address,
            'req_user:': req_user
        }
        return res
    
    @staticmethod
    def find_all(database: Session) -> List[object]:
        '''Função para fazer uma query de todas as Estacoes da DB'''
        stations = database.query(Station).all()
        res = []
        for station in stations:
            address = database.query(Address).filter(station.idEndereco==Address.idEndereco).first()
            aux ={
                'station': station,
                'address': address   
            }
            res.append(aux)

        return res
    
    @staticmethod
    def find_station_by_id(idPosto, database: Session) -> object:
        '''Função para fazer uma query de um posto pelo id da DB'''
        station = database.query(Station).filter(idPosto==Station.idPosto).first()
        address = database.query(Address).filter(station.idEndereco==Address.idEndereco).first()

        res = {
                'station': station,
                'address': address   
            }
        return res
    
    @staticmethod
    def find_address(idEndereco, database: Session) -> Address:
        '''Função para fazer uma query de um endereco da DB'''
        return database.query(Address).filter(idEndereco==Address.idEndereco).first()
    
    @staticmethod
    def update_station(old_station: Station, station: Station, address: Address, req_user: object, database: Session) -> object:
        try:
            station.idEndereco = old_station['address'].idEndereco
            address.idEndereco = old_station['address'].idEndereco
            station.idPosto = old_station['station'].idPosto
            database.merge(address)
            database.merge(station)
            database.commit()
            database.refresh(address)
            database.refresh(station)

        except:
            database.rollback()

        print(req_user.name)
        res = {
            'station': station,
            'address': address,
            'req_user:': req_user
        }
        return res
        
        # return station
    
    @staticmethod
    def delete_by_id(idPosto: int, req_user: object, database: Session) -> object:
        station = database.query(Station).filter(Station.idPosto == idPosto).first()
        address = database.query(Address).filter(Address.idEndereco == station.idEndereco).first()
        if station and address is not None:
            database.delete(station)
            database.commit()
            database.delete(address)
            database.commit()
            print(req_user.name)
            res = {
                'station': station,
                'address': address,
                'req_user:': req_user
            }
            return res
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Posto não existe"
            )
        