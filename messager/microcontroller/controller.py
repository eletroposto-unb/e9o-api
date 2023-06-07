from fastapi import APIRouter, status

from datetime import datetime


microcontroller  = APIRouter(
    prefix = '/microcontroller',
    tags = ['microcontroller'],
)

@microcontroller.get("/charge",
    status_code= status.HTTP_200_OK
)
def return_charge_status():
    '''
        This method returns the current charge status to station.
        As nowly this method is mocked, it changes the own status every 5 minutes.
        This method will return the status as follow:
            If the minute divided by 5 is odd then it will return 1
            and will return 0 otherwise.
        When this method returns 1, then the charge must be running
        If returns 0, then the charge must be stoepped.
    '''
    now = datetime.now()
    minute = now.time().minute
    print(f"Minute {minute}")
    print(f"Actual station state {(minute//5)}")
    return (minute//5)%2

@microcontroller.post("/totem/temperature",
    status_code = status.HTTP_202_ACCEPTED
)
def save_totem_temperature(request: float):
    '''Recieve temperature of the station totem in Celsius'''
    print(f"Totem temperature: {request} ºC")
    return request

@microcontroller.post("/totem/humidity",
    status_code = status.HTTP_202_ACCEPTED
)
def save_totem_humidity(request: float):
    '''Recieve humidity of the station in percentage'''
    print(f"Totem Humidity {request} %")
    return request

@microcontroller.post("/battery/temperature",
    status_code = status.HTTP_202_ACCEPTED
)
def save_battery_temperature(request: float):
    '''Recieve the temperature of battery in Celsius'''
    print(f"Battery temperature {request} ºC")
    return request

@microcontroller.post("/battery/voltage",
    status_code = status.HTTP_202_ACCEPTED
)
def save_battery_voltage(request: float):
    '''Recieve the battery voltage in Volts'''
    print(f"Battery voltage {request} V")
    return request

@microcontroller.post("/battery/current",
    status_code = status.HTTP_202_ACCEPTED
)
def save_battery_current(request: float):
    '''Recieve battry current in Ampere'''
    print(f"Battery current {request} A")
    return request

@microcontroller.post("/inverter/voltage",
    status_code = status.HTTP_202_ACCEPTED
)
def save_inverter_voltage(request: float):
    '''Recieve the inverter voltage in Volts'''
    print(f"Inverter voltage {request} V")
    return request

@microcontroller.post("/inverter/current",
    status_code = status.HTTP_202_ACCEPTED
)
def save_inverter_current(request: float):
    '''Recieve the inverter current in Ampere'''
    print(f"Inverter current {request} A")
    return request