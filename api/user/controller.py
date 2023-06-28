from fastapi import APIRouter, HTTPException, Request, status, Depends

from api.user.schema import UserRequest, UserResponse, UserRequestResponse, UserRequestListResponse, statusEnum
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
    response_model=UserRequestResponse
)
def find_one_by_cpf(
    req: Request,
    cpf,
    database: Session = Depends(get_database)
    ):

    if hasattr(req.state, 'exception'):
        return req.state.exception

    '''Procura um usuário pelo cpf'''
    user = UserRepository.find_by_key(cpf, database=database)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não existe não encontrado"
        )
    
    user.user_request = req.state.user
    return user

@users.get("/user/uid/{firebase_uid}",
    status_code = status.HTTP_200_OK,
    response_model=UserRequestResponse
)
def find_one_by_uid(
    req: Request,
    firebase_uid,
    database: Session = Depends(get_database)
    ):

    if hasattr(req.state, 'exception'):
        return req.state.exception
    
    '''Procura um usuário pelo firebase_uid'''
    user = UserRepository.find_by_uid(firebase_uid, database=database)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não existe não encontrado"
        )
    
    user.user_request = req.state.user
    return user

@users.get("/",
    status_code=status.HTTP_200_OK,
    response_model=None
)
def find_all(
    req: Request,
    database: Session = Depends(get_database)
    ):
    users = UserRepository.find_all(database=database)

    # print(request.state.user)

    # res = {
    #     'users': users,
    #     'user_request': req.state.user
    # }

    return users

@users.put("/{cpf}",
    status_code = status.HTTP_200_OK,
    response_model=UserRequestResponse
)
def update(
    cpf: str,
    request: UserRequest,
    req: Request,
    database: Session = Depends(get_database)
    ):

    if hasattr(req.state, 'exception'):
        return req.state.exception

    '''atualiza os dados do usuario'''
    user = UserRepository.find_by_key(cpf,database=database)
    if user.status == 'inactive':
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario inativo"
        )
    else:
        updated_user = UserRepository.update(user.firebase_uid, User(**request.dict()), database=database)
    
    setattr(updated_user, 'user_request', req.state.user)
    # BUG SEM ESSE PRINT ELE NÃO RETORNA USER_REQUEST
    print('Usuario que requisitou '+req.state.user.name)
    return updated_user

# Put não está alterando status
@users.put("/alterstatus/{cpf}",
    status_code = status.HTTP_200_OK,
    response_model=UserRequestResponse
)
def alter(
    req: Request,
    cpf,
    database: Session = Depends(get_database)
    ):

    if hasattr(req.state, 'exception'):
        return req.state.exception

    '''Alterna status do usuario. Dessa forma ao invés de deletar usuário, apenas desativa'''
    old_user = UserRepository.find_by_key(cpf, database=database)
    if old_user.status == 'inactive':
        old_user.status = 'active'
    else:
        old_user.status = 'inactive'

    print(old_user.status)
    updated_user = UserRepository.update_status(old_user, database)
    updated_user.user_request = req.state.user
    setattr(updated_user, 'user_request', req.state.user)
    # BUG SEM ESSE PRINT ELE NÃO RETORNA USER_REQUEST
    print('Usuario que requisitou '+req.state.user.name)
    return updated_user