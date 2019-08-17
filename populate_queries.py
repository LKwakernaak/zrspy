from datamodel import session, Appointment, Study, Course
from query import Query
import click

click.command()
def detect_courses():
    for name, study, course in session.query(Course.name, Course.study_key, Course.key).\
            filter(Course.study_key.in_([4403, # physics master
                                         4303, # astronomy master
                                         4081, # wiskunde propedeuse
                                         4061, # natuurkunde propedeuse
                                         4071, # sterrenkunde propedeuse
                                         4031, # informatica propedeuse
                                         4082, # wiskunde
                                         4062, # natuurkunde
                                         4072, # sterrenkunde
                                         4032  # informatica
                                         ])):
        course = course.replace('/', ' ').split(' ')[0]
        study = study.replace('/', ' ').split(' ')[0]
        query = Query(study+course)
        if ('course_key', course) not in query.selections:
            query.addselection('course_key', course)
        query.export()
