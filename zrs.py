import click
from scraper import update_db
from googlecalendar import tocalendar
from icalendar import to_ics

@click.group()
def main():
    pass

main.add_command(update_db)
main.add_command(tocalendar)
main.add_command(to_ics)
#
if __name__ == '__main__':
   main()
