import os
import click
import arrow
import datetime
import sqlalchemy
import pandas as pd

from ics import Calendar, Event


@click.command()
def to_ics(queryfile):
    click.echo("Fetching data")
    with open(queryfile) as f:
        sqlquery = f.read()

    engine = sqlalchemy.create_engine("sqlite:///data.db")
    data = pd.read_sql_query(sqlquery, engine)

    if len(data) == 0:
        click.secho("No matching appointments found. Try running zrspy update-db", fg='yellow')
        return

    calname = os.path.basename(queryfile).split('.')[0]


    calendar = Calendar()

    with click.progressbar(data.to_dict('records')) as bar:
        for i in bar:
            event = Event()
            event.name = "[{}] {}".format(i['Soort_act_'], i['Activiteit'])

            begin = arrow.get(' '.join([i['date'],i['start_time']]), "YYYY-MM-DD HH:mm")
            end = arrow.get(' '.join([i['date'], i['end_time']]), "YYYY-MM-DD HH:mm")

            event.begin = begin
            event.end = end
            event.description = """{Activiteit}
            Gebruiker {Gebruiker}
            Aanvrager {Aanvr_pers} {Aanvrager}
            Aanvraagnummer {Aanvr_nr}""".format(**i)

            calendar.events.add(event)

    click.echo('Writing to {}.ics'.format(calname))
    with open('{}.ics'.format(calname), 'w') as f:
        f.writelines(calendar)
    click.echo('Done!')




if __name__ == "__main__":
    cal = Calendar()
    event = Event()
    to_ics('lkwakernaak.sql')




