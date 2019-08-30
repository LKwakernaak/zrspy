# Installation
Zrspy can be run directly as a python script or by first installing. Within the project directory containing setup.py run:
```
pip install .
```
For flexibility install the project with the editable flag like so:
```
pip install --editable .
```
or
```
pip install -e .
```

You can then verify the installation with:
```
zrspy
```
Which should output the different command options.
```
Options:
  --help  Show this message and exit.

Commands:
  detect-courses
  query-editor
  to-gcal
  to-ics
  update-db
```

# Update-db
The first command to run. This command scrapes the room reservation system (zrs) to the local sqlite database file. The standard option for the command results in scraping by date (d m y). For example when trying to find out what classes are hosted for Ehrefests birthday:
```
zrspy update 18 1 2019
```
Grabbing multiple days is done with the --days flag (for a whole year):
```
zrspy update --days 365
```

# To-ics
The data obtained by the update-db command can then be used to generate icalendar .ics files. These can be imported in applications like google calendar and outlook and when hosted on a http server can by synchronised with to receive updates. A working example of such a web server can be found on www.lkwakernaak.nl/icals.
The ics files are formed by sql select statements in files stored in the queries folder. The file queries/na1.ics contains an example select statement for the physics and astronomy propedeuse year of 2019-2020.
To export ics files based on all queries run:
```
zrspy to-ics
```
. To convert a specific querie in a different folder type:
```
zrspy to-ics <filename>
```
.

# Detect-courses
When scraping the database the course keys for the general courses are extracted. By running
```
zrspy detect-courses
```
, individual queries for the courses of the bachelor and master level of physics astronomy mathmatics and informatics is generated and put into the queries folder.

# To-gcal
Depcrecated


# Query editor (beta)
A simple slightly buggy tool that helps in creating queries. Using the sqlite database viewer is recommanded.
The editor can be started with
```
zrspy query-editor
```
After which files can be created and edited. The tool offers a useful autocomplete function based on the unique entries in the database.
