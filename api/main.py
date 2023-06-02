from fastapi import FastAPI
from lib.dao.database import initialize_database

from api.user.controller import users
from api.car.controller import cars
from api.station_address.controller import stations

from fastapi.middleware.cors import CORSMiddleware

api = FastAPI()

origins = [
    "http://localhost:3000",
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(users)
api.include_router(cars)
api.include_router(stations)

@api.on_event("startup")
async def startup():
    initialize_database()
    

@api.get('/status')
async def index():
    return {"status": "online"}