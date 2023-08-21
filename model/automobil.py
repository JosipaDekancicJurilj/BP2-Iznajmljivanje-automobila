from . import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship

class Automobil (Base):
    __tablename__ = "automobili"
    ID = Column(Integer, primary_key =True)
    boja = Column(Text)
    broj_sjedala = Column(String(20))
    registracijska_oznaka = Column(Text)
    marka_automobila = Column(Text)

    id_proizvodaca = Column(Integer, ForeignKey('proizvodaci.ID'))
