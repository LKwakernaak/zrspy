import click
import logging
from scraper import update_db
# from googlecalendar import to_gcal
from icalendar import to_ics
from query import query_editor
import configparser
from populate_queries import detect_courses

@click.group(chain=True)
def main():
    pass

main.add_command(query_editor)
# main.add_command(to_gcal)
main.add_command(to_ics)
main.add_command(detect_courses)
main.add_command(update_db)
#
if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    loglevels = {
        'INFO' : logging.INFO,
        'DEBUG' : logging.DEBUG,
        'WARNING' : logging.WARNING,
        'ERROR' : logging.ERROR,
        'CRITICAL' : logging.CRITICAL
    }

    loglevel = loglevels[config['DEFAULT']['LogLevel']]

    logging.basicConfig(filename='zrspy.log', level=loglevel)

    main()
