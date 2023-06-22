from firebase_admin import credentials, firestore, initialize_app
from lib.config.env import settings
from enum import Enum

cred = credentials.Certificate(settings.firestore_key)
app = initialize_app(cred)
db = firestore.client()
stations_ref = db.collection(u'station')

class StationStatus(str, Enum):
    ONLINE = 'online'
    OFFLINE = 'offline'
    BUSY = 'busy'

class ChargeStatus(int, Enum):
    CHARGING = 1
    STOPPED = 0

class StationFields(str, Enum):
    totem_temperature = 'totem_temperature'
    totem_humidity = 'totem_humidity'
    battery_temperature = 'battery_temperature'
    battery_voltage = 'battery_voltage'
    battery_current = 'battery_current'
    inverter_voltage = 'inverter_voltage'
    inverter_current = 'inverter_current'

def get_firestore_doc(idStation: str):
    '''
        Return the document for station idStation 
    '''
    doc_ref = stations_ref.document(idStation)
    return doc_ref.get().to_dict()

def get_firestore_field(idStation: str, field: float) -> str:
    '''
        Get a value from a field into collections of Stations
    '''
    doc_ref = stations_ref.document(idStation)
    doc = doc_ref.get()
    return doc.to_dict()[field]

def set_firestore_field(idStation: str, field: str, value: float) -> None:
    '''
        Set a field with a value into collections of Stations
    '''
    doc_ref = stations_ref.document(idStation)
    doc = get_firestore_doc(idStation)
    doc[field] = value
    doc_ref.set(doc)

def check_temperature(idStation: str, temperature: float) -> None:
    status = get_firestore_field(idStation, 'status')
    if temperature > 50.0:
        status = StationStatus.OFFLINE
    print(f'Id Station {idStation}, Temperature: {temperature}, Status: {status}')
    set_firestore_field(idStation, 'status', status)

    
