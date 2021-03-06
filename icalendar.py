import os
import click
import arrow
import pandas as pd
import logging
from ics import Calendar, Event
from datamodel import engine

os.chdir(os.path.dirname(__file__))

def folder_to_ics():
    indir = 'queries/'
    outdir = 'icals/'
    for filename in os.listdir(indir):
        if filename.lower().endswith('.sql'):
            try:
                _to_ics(indir+filename, output_dir=outdir)
            except:
                print("{} invalid query file".format(indir+filename))

def _to_ics(queryfile, output_dir=None):

    with open(queryfile) as f:
        sqlquery = f.read()

    # engine = sqlalchemy.create_engine("sqlite:///data.db")
    data = pd.read_sql_query(sqlquery, engine)

    if len(data) == 0:
        click.secho("No matching appointments found in {}. Try running zrspy update-db".format(queryfile), fg='yellow')
        return

    calname = os.path.basename(queryfile).split('.')[0]

    calendar = Calendar()

    with click.progressbar(data.to_dict('records')) as bar:
        for i in bar:
            event = Event()
            event.name = "[{}] {}".format(i['soort_act'], i['activiteit'])

            try:
                begin = arrow.get(' '.join([i['date'], i['start_time']]), "YYYY-MM-DD HH:mm:ss")
                begin = begin.replace(tzinfo='Europe/Amsterdam')
                begin = begin.to('UTC')
                end = arrow.get(' '.join([i['date'], i['end_time']]), "YYYY-MM-DD HH:mm:ss")
                end = end.replace(tzinfo='Europe/Amsterdam')
                end = end.to('UTC')
            except DeprecationWarning:
                pass

            event.begin = begin
            event.end = end
            event.description = """{activiteit}
                Gebruiker {gebruiker}
                Aanvrager {aanvr_pers} {aanvrager}
                Aanvraagnummer {aanvr_nr}
                Locatie {locatie}""".format(**i)
            event.location = str(i['locatie'])

            calendar.events.add(event)

    logging.debug('Writing to {}.ics'.format(calname))
    with open('{}.ics'.format(output_dir+calname), 'w') as f:
        f.writelines(calendar)

@click.command()
@click.argument('queryfile', required=False)
def to_ics(queryfile):
    if queryfile is None:
        folder_to_ics()
    else:
        _to_ics(queryfile)





if __name__ == "__main__":
    cal = Calendar()
    event = Event()
    folder_to_ics()




