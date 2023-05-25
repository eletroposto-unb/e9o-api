from typing import List
from fastapi import APIRouter, HTTPException, status, Depends

from api.user.schema import UserRequest, UserResponse
from lib.dao.models.user import User
from lib.dao.repositories.user_repository import UserRepository
from lib.dao.database import get_database

from sqlalchemy.orm import Session

users = APIRouter(
    prefix = '/users',
    tags = ['users'],
    responses = {404: {"description": "Not found"}},
)

@users.post("/register/{firebase_uid}",
    status_code = status.HTTP_201_CREATED,
    response_model=UserResponse
)
def create(
    firebase_uid,
    request: UserRequest, 
    database: Session = Depends(get_database)
    ):
    '''Cria e salva um usuário'''
    user = UserRepository.create(firebase_uid, User(**request.dict()), database=database)
    return user

@users.get("/user/cpf/{cpf}",
    status_code = status.HTTP_200_OK,
    response_model=UserResponse
)
def find_one_by_cpf(
    cpf,
    database: Session = Depends(get_database)
    ):
    '''Procura um usuário pelo cpf'''
    user = UserRepository.find_by_key(cpf, database=database)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não existe não encontrado"
        )
    return UserResponse.from_orm(user)

@users.get("/user/uid/{firebase_uid}",
    status_code = status.HTTP_200_OK,
    response_model=UserResponse
)
def find_one_by_uid(
    firebase_uid,
    database: Session = Depends(get_database)
    ):
    '''Procura um usuário pelo firebase_uid'''
    user = UserRepository.find_by_uid(firebase_uid, database=database)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não existe não encontrado"
        )
    return UserResponse.from_orm(user)

@users.get("/",
    status_code=status.HTTP_200_OK,
    response_model=List[UserResponse]
)
def find_all(
    database: Session = Depends(get_database)
    ):
    users = UserRepository.find_all(database=database)
    return [UserResponse.from_orm(user) for user in users]

@users.put("/{cpf}",
    status_code = status.HTTP_200_OK,
    response_model=UserResponse
)
def update(
    cpf: str,
    request: UserRequest,
    database: Session = Depends(get_database)
    ):
    '''atualiza os dados do usuario'''
    user = UserRepository.find_by_key(cpf,database=database)
    if user.status == 'inactive':
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario inativo"
        )
    else:
        updated_user = UserRepository.update(user.firebase_uid, User(**request.dict()), database=database)
    return UserResponse.from_orm(updated_user)

@users.put("/alterstatus/{cpf}",
    status_code = status.HTTP_200_OK,
    response_model=UserResponse
)
def alter(
    cpf,
    database: Session = Depends(get_database)
    ):
    '''Alterna status do usuario. Dessa forma ao invés de deletar usuário, apenas desativa'''
    user = UserRepository.find_by_key(cpf, database=database)
    if user.status == 'inactive':
        user.status = 'active'
    else:
        user.status = 'inactive'
    user = UserRepository.update_status(user, database=database)
    return UserResponse.from_orm(user)