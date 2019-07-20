import click
from scraper import update_db
from googlecalendar import to_gcal
from icalendar import to_ics
from query import query_editor

@click.group()
def main():
    pass

main.add_command(update_db)
main.add_command(to_gcal)
main.add_command(to_ics)
main.add_command(query_editor)
#
if __name__ == '__main__':
   main()
