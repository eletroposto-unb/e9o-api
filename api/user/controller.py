from fastapi import APIRouter, status

from api.user.schema import UserRequest
from lib.dao.repositories import UserRepository

users = APIRouter(
    prefix = '/users',
    tags = ['users'],
    responses = {404: {"description": "Not found"}},
)

@users.post("/",
    status_code = status.HTTP_201_CREATED
)
def create(request: UserRequest):
    '''Cria e salva um usuário'''
    user = UserRepository.save(**request.dict())
    return user