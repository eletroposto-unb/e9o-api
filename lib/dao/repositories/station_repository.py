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