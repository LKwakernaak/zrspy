from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import click
import datetime


class client(): 
    @staticmethod
    def parse_table(table, day, month, year):
        table.dropna(how='all', inplace=True)
        table.reset_index(inplace=True)
        table['start_time'], table['end_time'] = zip(*table['Tijd'].map(lambda x: x.split(' ')))
        table['date'] = datetime.date(int(year), int(month), int(day))
        return table
    
    def startdriver(self):
        options = webdriver.ChromeOptions()
#        options.add_argument('headless')
        try:
            self.driver = webdriver.Chrome(chrome_options=options)
        except:
            self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
    
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
        go = self.driver.find_element_by_name("submit")
        self.setday(day)
        self.setmonth(month)
        self.setyear(year)
        go.click()
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        
        table = soup.find_all('table')[1]
        df = pd.read_html(str(table), header=0)[0]
        self.driver.back()
        df = self.parse_table(df, day, month, year)
        return df
    
    def grabpage(self, page_url, restart=True):
        self.driver.get(page_url)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        if self.errstring in soup:
            if restart:
                self.startdriver()
                self.grabpage(page_url, restart=False)
            else:
                print("Multiple bad requests for:",page_url)
    
    def __init__(self, *args, **kwargs):
        self.base_url = "http://zrs.leidenuniv.nl"
        self.errstring = "Start applicatie op de juiste manier!"
        self.startdriver()
        self.grabpage(self.base_url)

@click.command()
@click.argument('day', default=None, required=False)
@click.argument('month', default=None, required=False)
@click.argument('year', default=None, required=False)
@click.option('--days', default=None, help="The total number of days to fetch")
def main(day, month, year, days):
    c = client()
    
    click.echo("day {}\nmonth {}\nyear {}\ndays {}".format(day,month,year,days))
    
    today = datetime.date.today()
    
    if days is not None:
        click.echo('sequence of days')
        d = datetime.timedelta(days=1)
        date_list = [today + d*(i+1) for i in range(int(days))]
        
        for date in date_list:
            table = c.grabtable(date.day, date.month, date.year)
            click.echo(table.to_csv())
        
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


if __name__ == '__main__':
    main()
    