from . import Base
from sqlalchemy import *

class Proizvodac(Base):
    __tablename__ = "proizvodaci"
    ID = Column(Integer, primary_key=True)
    naziv = Column(String(50))
    web_stranica = Column(String(50))
    email = Column(String(100))
    telefon = Column(String(20))

