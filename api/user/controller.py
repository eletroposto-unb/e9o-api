from fastapi import APIRouter, status

from api.user.schema import UserRequest, UserResponse
from lib.dao.models.user import User
from lib.dao.repositories.user_repository import UserRepository

users = APIRouter(
    prefix = '/users',
    tags = ['users'],
    responses = {404: {"description": "Not found"}},
)

@users.post("/",
    status_code = status.HTTP_201_CREATED,
    response_model=UserResponse
)
def create(request: UserRequest):
    '''Cria e salva um usuário'''
    user = UserRepository.create(User(**request.dict()))
    return user