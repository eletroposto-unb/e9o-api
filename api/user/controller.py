from fastapi import APIRouter, HTTPException, status

from api.user.schema import UserRequest, UserResponse
from lib.dao.models.user import User
from lib.dao.repositories.user_repository import UserRepository

users = APIRouter(
    prefix = '/users',
    tags = ['users'],
    responses = {404: {"description": "Not found"}},
)

@users.post("/register/{firebase_uid}",
    status_code = status.HTTP_201_CREATED,
    response_model=UserResponse
)
def create(firebase_uid,request: UserRequest):
    '''Cria e salva um usuário'''
    user = UserRepository.create(firebase_uid, User(**request.dict()))
    return user

@users.get("/find/{cpf}",
    status_code = status.HTTP_200_OK,
    response_model=UserResponse
)
def find_one(cpf):
    '''Procura um usuário pelo cpf'''
    user = UserRepository.find_by_key(cpf)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não existe não encontrado"
        )
    return UserResponse.from_orm(user)

@users.get("/findall",
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponse]
)
def find_all():
    users = UserRepository.find_all()
    return [UserResponse.from_orm(user) for user in users]

@users.put("/update/{cpf}",
    status_code = status.HTTP_200_OK,
    response_model=UserResponse
)
def update(cpf, request: UserRequest):
    '''atualiza os dados do usuario'''
    user = UserRepository.find_by_key(cpf)
    if user.status == 'inactive':
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario inativo"
        )
    user = UserRepository.update(User(**request.dict()))
    return UserResponse.from_orm(user)