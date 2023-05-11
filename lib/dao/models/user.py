from sqlalchemy import BigInteger, Boolean, Column, Integer, String, Sequence

from lib.dao.database import Base

class User(Base):
    __tablename__ = 'users'
    
    id: int = Column(Integer, Sequence('users_seq'), primary_key=True, index=True)
    name: str = Column(String(100), nullable=False)
    surname: str = Column(String(100), nullable=False)
    email: str = Column(String(100), nullable=False)
    cpf: int = Column(BigInteger, nullable=False)
    is_admin: bool = Column(Boolean, default=False)
    telefone: int = Column(BigInteger, nullable=False)
    status: int = Column(Integer, nullable=False)

    
