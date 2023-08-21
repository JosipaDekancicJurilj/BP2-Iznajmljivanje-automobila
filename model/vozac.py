from . import Base
from sqlalchemy import *

class Vozac (Base):
    __tablename__ = "vozaci"
    ID = Column(Integer, primary_key=True)
    ime = Column(String(50))
    prezime = Column(String(50))
    adresa = Column(Text)
    telefon = Column(String(20))
    broj_vozacke_dozvole = Column(String(15))
    datum_vozackog_ispita = Column(Date)

    id_auto_skole = Column(Integer, ForeignKey('auto_skole.ID'))