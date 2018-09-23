#from selenium import webdriver
import os
from bs4 import BeautifulSoup
import pandas as pd
import click
import datetime
import requests
import sqlalchemy
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

class zrsclient(): 
    @staticmethod
    def parse_table(table, day, month, year):
        table.dropna(how='all', inplace=True)
        
        table['start_time'], table['end_time'] = zip(*table['Tijd'].map(lambda x: x.split(' ')))
        table['date'] = datetime.date(int(year), int(month), int(day))
#        table.drop('Tijd', inplace=True)
        
        columns = table.columns
        columns.drop('Aanvr.nr')
        
        aggregation_functions = {i:'first' for i in columns}
        aggregation_functions['Locatie'] = lambda x: ' '.join(x)
        
        table = table.groupby('Aanvr.nr').aggregate(aggregation_functions)#[['start_time'], ['end_time']].apply(lambda x: ' '.join(x)).reset_index()
#        print(table)
        table.drop_duplicates('Aanvr.nr', inplace=True)
        table.reset_index(inplace=True, drop=True)
        
        table.columns = [i.replace(' ','_').replace('.', '_') for i in columns]
        
        return table
    
    def update_db(self, table, day, month, year):
        # Remove date from previous table
        date = datetime.date(int(year), int(month), int(day))
        sql = "DELETE from appointments WHERE date='{:%Y-%m-%d}'".format(date)
        
        try:
            with self.engine.begin() as conn:
                conn.execute(sql)
        except:
            print('Created table')
        
        # Append to appointments
        table.to_sql('appointments', self.engine, if_exists='append', index=False)
        
    def getcookies(self):
        r = self.grabpage(self.base_url)
        self.cookies = r.cookies
    
#    def startdriver(self):
#        options = webdriver.ChromeOptions()
#        options.add_argument('headless')
#        try:
#            self.driver = webdriver.Chrome(chrome_options=options)
#        except:
#            self.driver = webdriver.Chrome()
#        self.driver.implicitly_wait(3)
    
    def _set(self, key, var):
        button = self.driver.find_element_by_name(key)
        for i in button.find_elements_by_tag_name('option'):
            option = i.text
            if str(option) == str(var):
                i.click()
                return
        # no setting found
        raise Exception("Incorrect date")
    
    def setday(self, day):
        self._set('day', day)
    def setmonth(self, month):
        self._set('month', month)
    def setyear(self, year):
        self._set('year', year)
    
    def grabtable(self, day, month, year):
#        go = self.driver.find_element_by_name("submit")
#        self.setday(day)
#        self.setmonth(month)
#        self.setyear(year)
#        go.click()
        data = {'day':int(day),
                'month':int(month),
                'year':int(year),
                'submit': 'Uitvoeren',
                'res_instantie': "_ALL_",
                'selgebouw': '_ALL_',
                'zrssort': 'aanvangstijd',
                'gebruiker':'',
                'aanvrager':'',
                'activiteit':''}
        
        r = requests.post(self.request_url, data=data, cookies=self.cookies)
        
        soup = BeautifulSoup(r.text, 'lxml')
        
#        print(soup)
        
        table = soup.find_all('table')[1]
        df = pd.read_html(str(table), header=0)[0]
#        self.driver.back()
        try:
            df = self.parse_table(df, day, month, year)
        except:
            print(df)

        self.update_db(df, day, month, year)
        
        
        return df
    
    def grabpage(self, page_url, restart=True):
#        self.driver.get(page_url)
        r = requests.get(page_url)
        soup = BeautifulSoup(r.text, 'lxml')
        if self.errstring in soup:
            if restart:
#                self.startdriver()
                self.grabpage(page_url, restart=False)
            else:
                print("Multiple bad requests for:",page_url)
        return r
    
    def __init__(self, *args, **kwargs):
        self.base_url = "http://zrs.leidenuniv.nl/ul/start.php"
        self.request_url = 'http://zrs.leidenuniv.nl/ul/query.php'
        self.errstring = "Start applicatie op de juiste manier!"
#        self.startdriver()
#        self.grabpage(self.base_url)
        self.getcookies()
        
        self.engine = sqlalchemy.create_engine("sqlite:///data.db")


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

@click.group()
def main():
    pass


@click.command()
@click.argument('day', default=None, required=False)
@click.argument('month', default=None, required=False)
@click.argument('year', default=None, required=False)
@click.option('--days', default=None, help="The total number of days to fetch")
def update(day, month, year, days):
    c = zrsclient()
    
    click.echo("day {}\nmonth {}\nyear {}\ndays {}".format(day,month,year,days))
    
    today = datetime.date.today()
    
    if days is not None:
        click.echo('sequence of days')
        d = datetime.timedelta(days=1)
        date_list = [today + d*(i+1) for i in range(int(days))]
        
        for date in date_list:
            table = c.grabtable(date.day, date.month, date.year)
#            click.echo(str(date.day), str(date.month), str(date.year))
            print(str(date.day), str(date.month), str(date.year))
        
    else:
        if day is None:
            day = today.day
        if month is None:
            day = today.month
        if year is None:
            year = today.year
        
        table = c.grabtable(day, month, year)
        click.echo(table.to_csv())
    return None

@click.command()
@click.argument('queryfile', required=True)
#@click.option('--file', '-f', default=None, help='Sqlite query selection from file')
def tocalendar(queryfile):
    click.echo('Fetching data')
    with open(queryfile) as f:
        sqlquery = f.read()
    
    engine = sqlalchemy.create_engine("sqlite:///data.db")
    data = pd.read_sql_query(sqlquery, engine)
    
    if len(data) == 0:
        click.secho("No matching appointments found. Try running zrspy update",fg='yellow')
        return
    
    click.echo("Authenticating google calendar connection")
    gcal = authenticate_gcal()
    
#    tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    calname = os.path.basename(queryfile).split('.')[0]
    body = {'summary':str(calname),
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
                    'summary': i['Soort_act_'][0]+' '+str(i['Activiteit']).split(' ',1)[1],
                    'location': i['Locatie'],
                    'description': i['Soort_act_']+i['Activiteit'],
                    'start': {
                            'dateTime':i['date']+'T'+i['start_time']+':00',
                            'timeZone': 'Europe/Amsterdam'
                            },
                    'end':{
                            'dateTime':i['date']+'T'+i['end_time']+':00',
                            'timeZone': 'Europe/Amsterdam'
                            },
                    }
            event = gcal.events().insert(calendarId=cal['id'], body=event).execute()
            
    click.echo("Done putting in {} appointments".format(len(data)))
            


main.add_command(update)
main.add_command(tocalendar)
#
#if __name__ == '__main__':
#    main()
#    