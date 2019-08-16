import click
from datamodel import session, Appointment, Study, Course

class Query():
    def __init__(self, name, directory='queries/'):
        self.name = str(name).split('.')[0]
        self.selections = []
        self.courses = set()
        self.studies = set()
        self.appointments = set()
        self.directory = directory
        self._getstudies()
        self._getcourses()
        self._getappointments()
        self._parsefile()

    def _getcourses(self):
        for course in session.query(Course):
            self.courses.add(course.key)

    def _getstudies(self):
        for studie in session.query(Study):
            self.studies.add(studie.key)

    def _getappointments(self):
        for appointment in session.query(Appointment.activiteit).distinct():
            self.appointments.add(appointment.activiteit)

    def _parsefile(self):
        syntax = [
            'from',
            'select',
            'where',
            '*',
            'or',
            'like'
        ]
        tables = []
        querries = []
        try:
            with open(self.directory+self.name+'.sql', 'r') as file:
                file.readline()
                for line in file:
                    line = line.split('--')[0] # remove comments
                    line = line.replace('`', '')
                    line = line.replace("'", '')
                    line = line.replace('"', '')
                    text = [i for i in line.split(None) if i.lower() not in syntax]
                    if len(text) == 2:
                        tables.append(text[0])
                        querries.append(text[1])

                self.selections = list(zip(tables, querries))
        except FileNotFoundError:
            # click.echo('New File')
            # with open(self.directory+self.name+'.sql', 'w') as file:
            pass


    def addselection(self, table, name):
        self.selections.append((table, name))

    @property
    def text(self):
        output = ""
        selections = self.selections.copy()
        if len(selections) > 0:
            output += "select * from appointments\n"
            output += "\twhere {} like '{}'\n".format(*selections.pop())
            while len(selections) > 0:
                output += "\tor {} like '{}'\n".format(*selections.pop())
        return output

    def export(self):
        with open(self.directory+self.name+'.sql', 'w') as file:
            file.writelines(self.text)


def autocompleted_input(choices=['aap','noot','mies']):
    """Asks te user for input and adds possible autocmpleted results.

    :param choices: list of strings containing all possible choices
    :return: input
    """

    # sys.stdout.write('starting\n')
    chars = []
    while True:
        newchar = click.getchar(False)
        # print(newchar)

        # try:
            # print(ord(newchar))

        if ord(newchar.encode()) == 3: # ctrl + c
            return

        elif ord(newchar) == 8: # backspace
            if len(chars) > 0:
                chars = chars[:-1]

        elif ord(newchar) == 9: # tab
            if len(autocomplete) > 0:
                chars = autocomplete[0]

        elif ord(newchar) == 13: # enter
            return "".join(chars)

        else:
            try:
                # newchar = newchar.decode('utf-8')
                chars.append(newchar)
            except:
                pass

        output = "".join(chars)

        if len(chars) > 0:
            autocomplete = [i for i in choices if str(i).startswith(output) and i != output]
            overflow = len(autocomplete) - 6
            if overflow > 0:
                autocomplete = autocomplete[:6]
                autocomplete.append(" +" + str(overflow))
        else:
            autocomplete = []
        click.clear()
        # sys.stdout.write('\r\r '*100)
        # sys.stdout.flush()
        # sys.stdout.write("\r\r" + output + ' ' + "\t".join(autocomplete))
        # sys.stdout.flush()
        # print(chars)
        print("\r\r" + output + ' ' + "\t".join(autocomplete)+'\t\t\t')

def choice_caroucel(choices=['aap', 'noot', 'mies']):
    index = 0
    length = len(choices)
    while True:
        click.echo("Choose with arrow keys {}".format(choices[index]))

        keypress = click.getchar()
        # print(keypress, len(keypress))
        if len(keypress) == 2: # possible arrow key depending on system
            index += 1
            index %= length
        elif ord(keypress) == 13: # enter
            return choices[index]
        elif ord(keypress) == 1:
            return False


@click.command()
def query_editor():
    filename = click.prompt("Filename")
    query = Query(filename)
    while True:
        click.secho("Current file", fg='yellow')
        click.echo(query.text)
        # autocompleted_input()
        choice = click.prompt("Choose:", type=click.Choice(['add', 'remove', 'save', 'close']))
        if str(choice).lower() == 'add':
            choices = {
                'activiteit' : query.appointments,
                'study_key' : query.studies,
                'course_key' : query.courses
            }
            column = click.prompt("Choose:", type=click.Choice(['activiteit', 'study_key', 'course_key']))
            click.echo('Select name, start typing. Press tab to autocomplete to first')
            # print(choices[column])
            value = autocompleted_input(choices[column])
            query.selections.append((column, value))
        elif str(choice) == 'remove': # remove
            choice = choice_caroucel(query.selections)
            if choice:
                click.prompt("Are you sure", type=click.Choice(["yes", "no"]))
                query.selections.remove(choice)

        elif str(choice) == 'save':
            query.export()

        elif str(choice) == 'close':
            exit()


if __name__ == "__main__":
    query_editor()
    # autocompleted_input()
    # query = Query('test')
    # query.addselection('study_key', '4061')
    # query.export()
