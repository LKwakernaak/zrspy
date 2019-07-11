import os
import time
import click
import pandas as pd

from httplib2 import Http
from googleapiclient.discovery import build
from oauth2client import file, client, tools

from datamodel import engine

def authenticate_gcal():
    """
    Dances the oath dance and returns a google calendar service client
    """
    SCOPES = "https://www.googleapis.com/auth/calendar"

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    return service


def listcals(service):
    items = []
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for entry in calendar_list['items']:
            items.append(entry)
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
    return items


@click.command()
@click.argument('queryfile', required=True)
def to_gcal(queryfile):
    click.echo('Fetching data')
    with open(queryfile) as f:
        sqlquery = f.read()

    # engine = sqlalchemy.create_engine("sqlite:///data.db")
    data = pd.read_sql_query(sqlquery, engine)

    if len(data) == 0:
        click.secho("No matching appointments found. Try running zrspy update-db", fg='yellow')
        return

    click.echo("Authenticating google calendar connection")
    gcal = authenticate_gcal()

    #    tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    calname = os.path.basename(queryfile).split('.')[0]
    body = {'summary': str(calname),
            'timeZone': 'Europe/Amsterdam'}

    for cal in listcals(gcal):
        if cal['summary'] == str(calname):
            click.secho("Deleting previous calendar {}".format(str(calname)), fg='red')
            gcal.calendars().delete(calendarId=str(cal['id'])).execute()

    click.echo("Creating calendar ", nl=False)
    click.secho(str(calname), fg='green')
    cal = gcal.calendars().insert(body=body).execute()

    click.echo('Populating calendar')
    with click.progressbar(data.to_dict('records')) as bar:
        for i in bar:
            event = {
                'summary': i['soort_act'][0] + ' ' + str(i['activiteit']).split(' ', 1)[1],
                'location': i['locatie'],
                'description': i['soort_act'] + i['activiteit'],
                'start': {
                    'dateTime': i['date'] + 'T' + i['start_time'] + ':00',
                    'timeZone': 'Europe/Amsterdam'
                },
                'end': {
                    'dateTime': i['date'] + 'T' + i['end_time'] + ':00',
                    'timeZone': 'Europe/Amsterdam'
                },
            }
            try:
                event = gcal.events().insert(calendarId=cal['id'], body=event).execute()
            except:
                time.sleep(1)
                event = gcal.events().insert(calendarId=cal['id'], body=event).execute()

    click.echo("Done putting in {} appointments".format(len(data)))