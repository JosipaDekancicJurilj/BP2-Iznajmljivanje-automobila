from sqlalchemy.orm import relationship

from .klijent import Klijent
from .ugovor import Ugovor
from .auto_skola import AutoŠkola
from .vozac import Vozac
from .proivodac import Proizvodac
from .automobil import Automobil
from .servis import Servis
from . import Base
from . import engine

Ugovor.klijent = relationship("Klijent", back_populates="ugovor")
Ugovor.automobil = relationship("Automobil", back_populates="ugovor")
Ugovor.vozac = relationship("Vozac", back_populates="ugovor")
Ugovor.servis = relationship("Servis", back_populates="ugovor")
Vozac.auto_skola = relationship("AutoŠkola", back_populates="vozaci")
Automobil.proizvodac = relationship("Proizvodac", back_populates = "automobili")
Proizvodac.automobil = relationship("Automobil", back_populates="proizvodaci")
Klijent.ugovor = relationship("Ugovor", back_populates = "klijenti")
Servis.ugovor = relationship("Ugovor", back_populates="servisi")
AutoŠkola.vozac = relationship("Vozac", back_populates="auto_skole")

Base.metadata.bind = engine
Base.metadata.create_all(bind=engine)