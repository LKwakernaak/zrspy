import sqlalchemy
from sqlalchemy import Column, Integer, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm
# from fuzzywuzzy import fuzz

engine = sqlalchemy.create_engine("sqlite:///data.db")
session = orm.sessionmaker(bind=engine)

Base = declarative_base()

"""CREATE TABLE appointments 
( "Tijd" TEXT, 
"Locatie" TEXT, 
"Soort_act_" TEXT, 
"Pers" FLOAT, 
"Tbv_" TEXT, 
"Groep" TEXT, 
"Activiteit" TEXT, 
"Gebruiker" TEXT, 
"Aanvrager" TEXT, 
"Aanvr_pers" TEXT, 
"Aanvr_nr" TEXT, 
start_time TEXT, 
end_time TEXT, 
date DATE )"""

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    Tijd = Column(String)
    Locatie = Column(String)
    Soort_act = Column(String)
    Pers = Column(Integer)
    Groep = Column(String)
    Activiteit = Column(String)
    Gebruiker = Column(String)
    Aanvrager = Column(String)
    Aanvr_pers = Column(String)
    Aanvr_nr = Column(String)
    start_time = Column(Time)
    end_time = Column(Time)
    date = Column(Date)

    def __repr__(self):
        return "<Appointment(Activiteit={}, Tijd={}, Locatie={})>".\
                        format(self.Activiteit,
                               self.Tijd,
                               self.Locatie)




def find_typo():
    pass

if __name__ == '__main__':
    appointment = Appointment()
    print(appointment)