from sqlalchemy import Column, Integer, String, Sequence

from lib.dao.database import Base

class User(Base):
    __tablename__ = 'users'
    
    id: int = Column(Integer, Sequence('users_seq'), primary_key=True, index=True)
    name: str = Column(String(100), nullable=False)
    
