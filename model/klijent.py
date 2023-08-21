from . import Base

from sqlalchemy import *

class Klijent (Base):
    __tablename__ = "klijenti"
    ID = Column(Integer, primary_key = True)
    ime = Column(String(50))
    prezime = Column(String(50))
    adresa = Column(String(100))
    telefon = Column(String(50))

    