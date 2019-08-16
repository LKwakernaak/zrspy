import os
import sqlalchemy
from sqlalchemy import Column, Integer, String, Date, Time, text, func, ForeignKey, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import logging

import configparser

os.chdir(os.path.dirname(__file__))

config = configparser.ConfigParser()
config.read('config.ini')
data_url = config['DEFAULT']['DatabaseURL']

# from fuzzywuzzy import fuzz

engine = sqlalchemy.create_engine(data_url)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

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
    tijd = Column(String)
    locatie = Column(String)
    soort_act = Column(String)
    pers = Column(Integer)
    tbv = Column(String)
    groep = Column(String)
    activiteit = Column(String)
    gebruiker = Column(String)
    aanvrager = Column(String)
    aanvr_pers = Column(String)
    aanvr_nr = Column(String)
    bezetting = Column(String)
    start_time = Column(Time)
    end_time = Column(Time)
    date = Column(Date)
    course_key = Column(String, ForeignKey('courses.key'))
    study_key = Column(String, ForeignKey('studies.key'))

    def __repr__(self):
        return "<Appointment(Activiteit={}, Tijd={}, Locatie={})>".\
                        format(self.activiteit,
                               self.tijd,
                               self.locatie)

class Study(Base):
    __tablename__ = 'studies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    key = Column(String, unique=True)
    appointments = relationship('Appointment')
    courses = relationship('Course')

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    key = Column(String, unique=True)
    study_key = Column(String, ForeignKey('studies.key'))
    appointments = relationship('Appointment')


Base.metadata.create_all(engine)

session = Session()

def find_keys(appointment):
    if type(appointment) is not type(str()):
        return None, None
    candidate = appointment.split()[0]
    candidate_study_key = candidate[:4]
    candidate_course_key = candidate[4:]
    if candidate_study_key.isnumeric() and len(candidate_study_key)==4: # starts with a 4 digit number so is probably a study
        return candidate_study_key, candidate_course_key
    else:
        return None, None


def parse_appointments():
    for appointment in session.query(Appointment)\
            .filter(Appointment.study_key.isnot(None))\
            .group_by(Appointment.study_key):
        candidate_study_key = str(appointment.study_key)

        if not session.query(Study).filter_by(key=candidate_study_key).first():  # study exists in db
            session.add(Study(key=str(candidate_study_key)))
            logging.info('New study: {}'.format(candidate_study_key))

    for appointment in session.query(Appointment)\
            .filter(Appointment.course_key.isnot(None))\
            .group_by(Appointment.course_key):
        candidate_study_key = str(appointment.study_key)
        candidate_course_key = str(appointment.course_key)

        if not session.query(Course).filter_by(key=candidate_course_key).first():
            session.add(
                Course(key=str(candidate_course_key), name=str(" ".join(appointment.activiteit.split()[1:])), study_key=str(candidate_study_key)))
            logging.info('New Course {}'.format(candidate_course_key))

    session.commit()



# def find_typo():
#     courses = [course for course in session.query(Appointment.course_key, func.count(Appointment.course_key)).group_by(Appointment.course_key)]
#     print(courses)

if __name__ == '__main__':
    parse_appointments()
    # find_typo()
    # print(fuzz.ratio('aap', 'mantequilla'))