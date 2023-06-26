from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from api.user.controller import users
from api.car.controller import cars
from api.wallet.controller import wallets
from api.station_address.controller import stations
from api.dependencies.verifyuser import verify_user

from lib.config.env import settings
from lib.dao.database import initialize_database


import firebase_admin
from firebase_admin import auth

api = FastAPI(dependencies=[Depends(verify_user)])

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
api.include_router(wallets)

@api.middleware("http")
async def teste(request: Request, call_next):
    print("Verificação do token")

    print(request.url.path)

    # print(request.path_params)

    if not firebase_admin._apps:
        credential = firebase_admin.credentials.Certificate(settings.firebase_file+'.json')
        firebase_admin.initialize_app(credential)


    auth_token = request.headers.get('authorization')
    # print(auth_token)
    
    if (auth_token):
        bearer_token: str = auth_token.split('Bearer')[1].strip()
        headers = {"authorization": "Bearer " + bearer_token}

        res = auth.verify_id_token(bearer_token)

        request.state.uid = res['user_id']
    else:
        return JSONResponse(content='Token necessario', status_code=status.HTTP_401_UNAUTHORIZED)
            
    return await call_next(request)

@api.on_event("startup")
async def startup():
    initialize_database()
    

@api.get('/status')
async def index():
    return {"status": "online"}