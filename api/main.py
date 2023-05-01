from fastapi import FastAPI
from lib.dao.database import initialize_database

from api.user.controller import users

api = FastAPI()

api.include_router(users)

@api.on_event("startup")
async def startup():
    initialize_database()
    

@api.get('/status')
async def index():
    return {"status": "online"}