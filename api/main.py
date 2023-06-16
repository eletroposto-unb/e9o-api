from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from lib.dao.database import initialize_database, get_database

from api.user.controller import users
from api.car.controller import cars
from api.station_address.controller import stations

from lib.dao.repositories.user_repository import UserRepository

from fastapi.middleware.cors import CORSMiddleware

import firebase_admin
from firebase_admin import auth

api = FastAPI()

origins = [
    'http://localhost:3000'
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

whitelist = [
    {
        'route': '/stations/',
        'method': 'GET'
    },
    {
        'route': '/stations/station/{idPosto}',
        'method': 'GET'
    },
    {
        'route': '/stations/station/address/{idEndereco}',
        'method': 'GET'
    },
    {
        'route': '/users/',
        'method': 'GET'
    },
    {
        'route': '/cars/',
        'method': 'GET'
    },
    {
        'route': '/cars/',
        'method': 'POST'
    },
    {
        'route': '/cars/',
        'method': 'PUT'
    },
    {
        'route': '/cars/',
        'method': 'DELETE'
    },
]

@api.middleware("http")
async def teste(request: Request, call_next):
    print("Verificação do token")

    print(request.path_params)

    if not firebase_admin._apps:
        credential = firebase_admin.credentials.Certificate('eletroposto-e9o-firebase-adminsdk-vgpsy-d158db5099.json')
        firebase_admin.initialize_app(credential)


    auth_token = request.headers.get('authorization')
    
    if (auth_token):
        bearer_token: str = auth_token.split('Bearer')[1].strip()
        headers = {"authorization": "Bearer " + bearer_token}

        res = auth.verify_id_token(bearer_token)

        uid = res['user_id']

        user = UserRepository.find_by_uid(uid, database=get_database())
        if (not user):
            json_user = jsonable_encoder(user)
            print(json_user)
            return JSONResponse(content=json_user, status_code=status.HTTP_404_NOT_FOUND)
        
        elif(user.is_admin == False):
            if not any(request.url.path.startswith(obj['route']) and obj['method'] == request.method for obj in whitelist):
                json_user = jsonable_encoder(user)
                print(json_user)
                return JSONResponse(content=json_user, status_code=status.HTTP_401_UNAUTHORIZED)
            
    return await call_next(request)

@api.on_event("startup")
async def startup():
    initialize_database()
    

@api.get('/status')
async def index():
    return {"status": "online"}