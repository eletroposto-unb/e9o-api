from fastapi import FastAPI
from lib.dao.database import initialize_database
from fastapi.middleware.cors import CORSMiddleware

from messager.microcontroller.controller import microcontroller
from lib.firestore.firestore import set_firestore_field

messager = FastAPI()

origins = [
    "http://localhost:3000",
]

messager.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

messager.include_router(microcontroller)

@messager.on_event("startup")
async def startup():
    initialize_database()
    set_firestore_field('1', 'charge', '1')
    

@messager.get('/status')
async def index():
    return {"status": "online"}