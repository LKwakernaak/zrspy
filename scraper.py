from bs4 import BeautifulSoup
import pandas as pd
import click
import datetime
import requests
import sqlalchemy
from multiprocessing import Pool

from datamodel import engine

class Scraper():
    @staticmethod
    def parse_table(table, day, month, year):
        table.dropna(how='all', inplace=True)

        table['start_time'], table['end_time'] = zip(*table['Tijd'].map(lambda x: x.split(' ')))
        table['date'] = datetime.date(int(year), int(month), int(day))
        #        table.drop('Tijd', inplace=True)

        columns = table.columns
        columns.drop('Aanvr.nr')

        aggregation_functions = {i: 'first' for i in columns}
        aggregation_functions['Locatie'] = lambda x: ' '.join(x)

        table = table.groupby('Aanvr.nr').aggregate(
            aggregation_functions)  # [['start_time'], ['end_time']].apply(lambda x: ' '.join(x)).reset_index()
        table.drop_duplicates('Aanvr.nr', inplace=True)
        table.reset_index(inplace=True, drop=True)

        table.columns = [i.replace(' ', '_').replace('.', '_') for i in columns]

        mapping = {
            "Tijd": "tijd",
            "Locatie": "locatie",
            "Soort_act_": "soort_act",
            "Pers": "bezetting",
            "Tbv_": "tbv",
            "Groep": "groep",
            "Activiteit": "activiteit",
            "Gebruiker": "gebruiker",
            "Aanvrager": "aanvrager",
            "Aanvr_pers": "aanvr_pers",
            "Aanvr_nr": "aanvr_nr"
        }

        table = pd.DataFrame(table)
        table.rename(index=str, columns=mapping, inplace=True)
        table['start_time'] += ":00"
        table['end_time'] += ":00"

        # table['start_time'] = pd.to_datetime(table['start_time'])
        # table['end_time'] = pd.to_datetime(table['end_time'])

        return table

    def update_db(self, table, day, month, year):
        # Remove date from previous table
        date = datetime.date(int(year), int(month), int(day))
        sql = "DELETE from appointments WHERE date='{:%Y-%m-%d}'".format(date)

        try:
            with engine.begin() as conn:
                conn.execute(sql)
        except:
            print('Created table')

        # Append to appointments
        table.to_sql('appointments', engine, if_exists='append', index=False)

    def getcookies(self):
        r = self.session.get(self.base_url, allow_redirects=False)
        r = self.session.get(self.referer)

        soup = BeautifulSoup(r.text, 'html.parser')
        hidden_tag = soup.find('input', type='hidden')

        self.crsf_token = hidden_tag.attrs['value']

        self.cookies = r.cookies

    def setday(self, day):
        self._set('day', day)

    def setmonth(self, month):
        self._set('month', month)

    def setyear(self, year):
        self._set('year', year)

    def grabtable(self, day, month, year, update=True):
        data = {'csrf_token': self.crsf_token,
                'day': int(day),
                'month': int(month),
                'year': int(year),
                'submit': 'Uitvoeren',
                'res_instantie': "_ALL_",
                'selgebouw': '_ALL_',
                'zrssort': 'aanvangstijd',
                'gebruiker': '',
                'aanvrager': '',
                'activiteit': ''}

        self.session.headers["Referer"] = self.referer

        r = self.session.post(self.request_url, data=data, headers={"Referer":self.referer})
        r.raise_for_status()

        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find_all('table')[1]
        df = pd.read_html(str(table), header=0)[0]
        #        self.driver.back()
        try:
            df = self.parse_table(df, day, month, year)
        except:
            print("Error parsing table\n",df)
        if update:
            self.update_db(df, day, month, year)

        return df

    def grabpage(self, page_url, restart=True):
        #        self.driver.get(page_url)
        r = self.session.get(page_url)
        soup = BeautifulSoup(r.text, 'lxml')
        if self.errstring in soup:
            if restart:
                #                self.startdriver()
                self.grabpage(page_url, restart=False)
            else:
                print("Multiple bad requests for:", page_url)
        return r

    def __init__(self, *args, **kwargs):
        self.base_url = "https://zrs.leidenuniv.nl"#/ul/start.php"
        self.referer = "https://zrs.leidenuniv.nl/ul/start.php"
        self.request_url = 'https://zrs.leidenuniv.nl/ul/query.php'
        self.errstring = "Start applicatie op de juiste manier!"

        self.session = requests.session()
        self.getcookies()
        self.grabpage(self.base_url)
        #        self.startdriver()
        #        self.grabpage(self.base_url)
        # self.getcookies()

        # self.engine = sqlalchemy.create_engine("sqlite:///data.db")


@click.command()
@click.argument('day', default=None, required=False)
@click.argument('month', default=None, required=False)
@click.argument('year', default=None, required=False)
@click.option('--days', default=None, help="The total number of days to fetch")
def update_db(day, month, year, days):
    scraper = Scraper()

    click.echo("day {}\nmonth {}\nyear {}\ndays {}".format(day, month, year, days))

    today = datetime.date.today()

    if days is not None:
        click.echo('sequence of days')
        d = datetime.timedelta(days=1)
        date_list = [today + d * (i + 1) for i in range(int(days))]

        with Pool(30) as p:
            for date in date_list:
                table = scraper.grabtable(date.day, date.month, date.year)
                #            click.echo(str(date.day), str(date.month), str(date.year))
                print(str(date.day), str(date.month), str(date.year))

    else:
        if day is None:
            day = today.day
        if month is None:
            day = today.month
        if year is None:
            year = today.year

        table = scraper.grabtable(day, month, year)
        click.echo(table.to_csv())

    print("Done!")
    return None

if __name__ == '__main__':
    scraper = Scraper()

    today = datetime.datetime.today().date()
    print(today)

    print(scraper.grabtable(today.day+1,today.month,today.year))
    print(scraper.session.cookies)

    update_db(1,1,1,120)