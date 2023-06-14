from fastapi import FastAPI, Request
from lib.dao.database import initialize_database

from api.user.controller import users
from api.car.controller import cars
from api.station_address.controller import stations

from fastapi.middleware.cors import CORSMiddleware

import firebase_admin
from firebase_admin import auth

from lib.config.env import settings



import requests

api = FastAPI()

origins = [
    "*",
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

@api.middleware("http")
async def teste(request: Request, call_next):
    print("Verificação do token")

    if not firebase_admin._apps:
        credential = firebase_admin.credentials.Certificate('eletroposto-e9o-firebase-adminsdk-vgpsy-1aaa035bc8.json')
        firebase_admin.initialize_app(credential)

    default_app = firebase_admin.get_app(name='[DEFAULT]')
    auth_token = request.headers.get('authorization')
    
    if (auth_token):
        bearer_token: str = auth_token.split('Bearer')[1].strip()
        headers = {"authorization": "Bearer " + bearer_token}

        res = auth.verify_id_token(bearer_token)
        print(res)

    return await call_next(request)
    # print("middleware retornar usuario fazendo request")
    # print(request.auth)
    # response = await call_next(request)
    # return response

@api.on_event("startup")
async def startup():
    initialize_database()
    

@api.get('/status')
async def index():
    return {"status": "online"}