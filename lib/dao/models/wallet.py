from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer, String, Sequence

from lib.dao.database import Base
from lib.dao.models.user import User

class Wallet(Base):
    __tablename__ = 'wallets'
    
    idCarteira: int = Column(Integer, Sequence('seq_wallet_table', start=1) ,primary_key=True, index=True)
    qtdCreditos: int = Column(Integer, default=30)
    qtdCreditosSolicitados: int = Column(Integer, default=0)
    cpf: str = Column(String(11), ForeignKey(User.cpf), nullable=False)
    