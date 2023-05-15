from sqlalchemy import BigInteger, Boolean, Column, Integer, String, Sequence

from lib.dao.database import Base

class User(Base):
    __tablename__ = 'users'
    
    firebase_uid: str = Column(String(128))
    name: str = Column(String(100), nullable=False)
    surname: str = Column(String(100), nullable=False)
    email: str = Column(String(100), nullable=False)
    cpf: str = Column(String(100), primary_key=True, nullable=False, index=True)
    is_admin: bool = Column(Boolean, default=False)
    telefone: int = Column(String(100), nullable=False)
    status: str = Column(String(10), nullable=False)

    
