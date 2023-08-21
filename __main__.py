from model import *
from model.relacije import *
from model.cache import region, api


ID = 2
KEY = f'automobil_{ID}'
marka = region.get(KEY)
print(marka)
if marka is api.NO_VALUE:
    marka = session.query(Automobil).filter(Automobil.ID_automobila==ID).one()
    region.set(KEY, marka)
print(marka.naziv + " " + marka.model)