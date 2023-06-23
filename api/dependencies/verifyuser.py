from fastapi import Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from lib.dao.database import get_database
from lib.dao.repositories.user_repository import UserRepository
from sqlalchemy.orm import Session

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

def verify_user(request: Request, database: Session = Depends(get_database)):
  uid = request.state.uid
  user = UserRepository.find_by_uid(uid, database=database)
  if (not user or user.status == 'inactive'):
      json_user = jsonable_encoder(user)
      print(json_user)
      return JSONResponse(content=json_user, status_code=status.HTTP_404_NOT_FOUND)
  
  elif(user.is_admin == False and user.status == 'active'):
      if not (request.url.path.startswith(obj['route']) and obj['method'] == request.method for obj in whitelist):
          json_user = jsonable_encoder(user)
          print(json_user)
          return JSONResponse(content=json_user, status_code=status.HTTP_403_FORBIDDEN)
  else:
      request.state.user = user
      return user