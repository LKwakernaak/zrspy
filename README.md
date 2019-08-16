# Installation
Zrspy can be can as a from the command line like:
```
python zrs.py update --days 120
```
Or by first installing it (while zrs.py parent directory)
```
pip install .
```
In case you want to mess around with zrspy add the development flag
```
pip install --editable .
```
or
```
pip install -e .
```

When that is complete you can run zrspy from anywhere as a system command:
```
zrspy update --days 120
```
# Scrape zrs
Scraping the zrs is done with zrs update. The standard option for scraping is scraping by date (d m y). For example when trying to find out what classes are hosted for Ehrefests birthday:
```
zrspy update 18 1 2019
```
Grabbing multiple days is done with the days flag like so (for a whole year):
```
zrspy update --days 365
```
These dates are stored to a sqlite db file named data.db. When the information of a date is added to the database the old entries on that date are removed.


# Export to google calendar
Exporting to google calendar is done with the to_gcal command. This command requires a sql query as input. Supplied is the example.sql file that adds all physics masters classes of 2018-2019. All these classes have a class-number that starts with 4403 which is the filter used in the example:
```
zrspy to_gcal example.sql
```
The sql query file contains:
```sql
SELECT *
FROM appointments  -- Semester 1
WHERE `Activiteit` LIKE '%4403%' --All physics masters of 18-19 start with 4403
;
```
