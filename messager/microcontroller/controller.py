from datetime import datetime, timedelta
from fastapi import APIRouter, status

from lib.firestore.firestore import ChargeStatus, check_temperature, get_firestore_field, set_firestore_field, StationFields


microcontroller  = APIRouter(
    prefix = '/microcontroller',
    tags = ['microcontroller'],
)

@microcontroller.get("/{idStation}/charge",
    status_code= status.HTTP_200_OK
)
def return_charge_status(idStation: str):
    '''
        This method returns the current charge status to station.
        As nowly this method is mocked, it changes the own status every 5 minutes.
        This method will return the status as follow:
            If the minute divided by 5 is odd then it will return 1
            and will return 0 otherwise.
        When this method returns 1, then the charge must be running
        If returns 0, then the charge must be stoepped.
    '''
    charge_start_time = get_firestore_field(idStation, StationFields.charge_start_time)
    charge_time = get_firestore_field(idStation, StationFields.charge_time)

    now = datetime.now()
    charge_end_time = charge_start_time + timedelta(minutes=charge_time)
    charge_end_time = datetime.isoformat(charge_end_time)
    charge_end_time = charge_end_time[:26]
    charge_end_time = datetime.fromisoformat(charge_end_time)
    if now > charge_end_time:
        set_firestore_field(idStation, StationFields.charge, ChargeStatus.STOPPED)
    charge_status = get_firestore_field(idStation, StationFields.charge)
    return charge_status

@microcontroller.post("/{idStation}/totem/temperature",
    status_code = status.HTTP_202_ACCEPTED
)
def save_totem_temperature(idStation: str, request: float):
    '''Recieve temperature of the station totem in Celsius'''
    set_firestore_field(idStation, StationFields.totem_temperature, request)
    check_temperature(idStation, request)
    print(f"Totem temperature: {request} ºC")
    return request

@microcontroller.post("/{idStation}/totem/humidity",
    status_code = status.HTTP_202_ACCEPTED
)
def save_totem_humidity(idStation: str, request: float):
    '''Recieve humidity of the station in percentage'''
    set_firestore_field(idStation, StationFields.totem_humidity, str(request))
    print(f"Totem Humidity {request} %")
    return request

@microcontroller.post("/{idStation}/battery/temperature",
    status_code = status.HTTP_202_ACCEPTED
)
def save_battery_temperature(idStation: str, request: float):
    '''Recieve the temperature of battery in Celsius'''
    set_firestore_field(idStation, StationFields.battery_temperature, request)
    check_temperature(idStation, request)
    print(f"Battery temperature {request} ºC")
    return request

@microcontroller.post("/{idStation}/battery/voltage",
    status_code = status.HTTP_202_ACCEPTED
)
def save_battery_voltage(idStation: str, request: float):
    '''Recieve the battery voltage in Volts'''
    set_firestore_field(idStation, StationFields.battery_voltage, request)
    print(f"Battery voltage {request} V")
    return request

@microcontroller.post("/{idStation}/battery/current",
    status_code = status.HTTP_202_ACCEPTED
)
def save_battery_current(idStation: str, request: float):
    '''Recieve battry current in Ampere'''
    set_firestore_field(idStation, StationFields.battery_current, request)
    print(f"Battery current {request} A")
    return request

@microcontroller.post("/{idStation}/inverter/voltage",
    status_code = status.HTTP_202_ACCEPTED
)
def save_inverter_voltage(idStation: str, request: float):
    '''Recieve the inverter voltage in Volts'''
    set_firestore_field(idStation, StationFields.inverter_voltage, request)
    print(f"Inverter voltage {request} V")
    return request

@microcontroller.post("/{idStation}/inverter/current",
    status_code = status.HTTP_202_ACCEPTED
)
def save_inverter_current(idStation: str, request: float):
    '''Recieve the inverter current in Ampere'''
    set_firestore_field(idStation, StationFields.inverter_current, request)
    print(f"Inverter current {request} A")
    return request