from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from lib.dao.database import get_database
from lib.dao.repositories.user_repository import UserRepository
from lib.config.env import settings

from sqlalchemy.orm import Session

import firebase_admin
from firebase_admin import auth

whitelist = [
    {
        'route': '/stations/',
        'method': 'GET'
    },
    {
        'route': '/stations/station/',
        'method': 'GET'
    },
    {
        'route': '/stations/station/address/',
        'method': 'GET'
    },
    {
        'route': '/stations/activate/',
        'method': 'POST'
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
    {
        'route': '/wallet/register/',
        'method': 'POST'
    },
    {
        'route': '/wallet/credits/',
        'method': 'GET'
    },
    {
        'route': '/wallet/creditosSolicitados/',
        'method': 'PUT'
    }
]

# def verify_user(request: Request, database: Session = Depends(get_database)):
#     uid = request.state.uid
#     user_request = UserRepository.find_by_uid(uid, database=database)

#     if (not user_request or user_request.status == 'inactive'):
#         request.state.exception = JSONResponse(content=jsonable_encoder({'detail':'Usuário não existe não encontrado'}),status_code=status.HTTP_404_NOT_FOUND)
    
#     elif(user_request.is_admin == False and user_request.status == 'active'):
#         if not (request.url.path.startswith(obj['route']) and obj['method'] == request.method for obj in whitelist):
#             json_user = jsonable_encoder(user_request)
#             print(json_user)
#             request.state.exception = JSONResponse(content=jsonable_encoder({'detail': 'Usuario'+json_user.name+'nao tem permissao'}), status_code=status.HTTP_403_FORBIDDEN)
#     else:
#         request.state.user = user_request
#         return user_request

def verify_user_uid(request: Request, database: Session):
    uid = request.state.uid
    user_request = UserRepository.find_by_uid(uid, database=database)

    if (not user_request or user_request.status == 'inactive'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Sem autorização"
          )
    
    elif(user_request.is_admin == False and user_request.status == 'active'):
        if not (request.url.path.startswith(obj['route']) and obj['method'] == request.method for obj in whitelist):
          raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Sem autorização"
          )
    return user_request
    
def tokenToUser(request: Request, database: Session = Depends(get_database)):
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
    
    user = verify_user_uid(request, database)

    return user