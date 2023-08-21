from . import Base
from sqlalchemy import *

class AutoŠkola (Base):
    __tablename__ = "auto_skole"
    ID = Column(Integer, primary_key =True)
    id_broj = Column(String(10))
    naziv = Column(String(50))
    adresa = Column(String(100))
    telefon = Column(String(20))