import sqlalchemy
from sqlalchemy import Column, Integer, String, Date, Time, text, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from fuzzywuzzy import fuzz

engine = sqlalchemy.create_engine("sqlite:///data1.db")
Session = sessionmaker(bind=engine)

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
    Soort_act_ = Column(String)
    Pers = Column(Integer)
    Groep = Column(String)
    Activiteit = Column(String)
    Gebruiker = Column(String)
    Aanvrager = Column(String)
    Aanvr_pers = Column(String)
    Aanvr_nr = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    date = Column(Date)
    course_key = Column(String, ForeignKey('courses.key'))
    study_key = Column(String, ForeignKey('studies.key'))

    def __repr__(self):
        return "<Appointment(Activiteit={}, Tijd={}, Locatie={})>".\
                        format(self.Activiteit,
                               self.Tijd,
                               self.Locatie)

class Study(Base):
    __tablename__ = 'studies'

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    appointments = relationship('Appointment')
    courses = relationship('Course')

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    Activiteit = Column(String, unique=True)
    key = Column(String)
    study_key = Column(String, ForeignKey('studies.key'))
    appointments = relationship('Appointment')


Base.metadata.create_all(engine)

session = Session()

def parse_appointments():
    for count, appointment in session.query(func.count(Appointment.Activiteit), Appointment.Activiteit)\
            .group_by(Appointment.Activiteit):
        candidate = appointment.split()[0]
        candidate_study_key = candidate[:4]
        candidate_course_key = candidate[4:]
        if candidate_study_key.isnumeric() and len(candidate_study_key)==4: # starts with a 4 digit number so is probably a study
            if not session.query(Study).filter_by(key=candidate_study_key).first(): # study exists in db
                session.add(Study(key=candidate_study_key))

            if not session.query(Course).filter_by(key=candidate).first():
                session.add(Course(key=candidate_course_key, Activiteit=appointment, study_key=candidate_study_key))
    session.commit()



def find_typo():
    courses = [course for course in session.query(Appointment.course_key, func.count(Appointment.course_key)).group_by(Appointment.course_key)]
    print(courses)

if __name__ == '__main__':
    parse_appointments()
    find_typo()
    print(fuzz.ratio('aap', 'mantequilla'))