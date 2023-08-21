from . import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship

class Ugovor(Base):
    __tablename__ = "ugovori"
    ID = Column(Integer, primary_key=True)
    cijena = Column(Text)
    datum_pocetka = Column(Date)
    datum_zavrsetka = Column(Date)

    id_automobila = Column(Integer, ForeignKey('automobili.ID'))
    id_klijenta = Column(Integer, ForeignKey('klijenti.ID'))
    id_vozaca = Column(Integer, ForeignKey('vozaci.ID'))
    id_servisa = Column(Integer, ForeignKey('servisi.ID'))