
from . import Base
from sqlalchemy import *

class Servis (Base):
    __tablename__ = "servisi"
    ID = Column(Integer, primary_key = True)
    vrsta_servisa = Column(Text)
    datum_servisa = Column(DateTime)
    mjesto_servisa = Column(Text)
