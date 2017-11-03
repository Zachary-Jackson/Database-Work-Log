import datetime
import os

from peewee import *

current_location = os.path.dirname(os.path.abspath(__file__))
file_location = os.path.join(current_location, 'database.db')
db = SqliteDatabase(file_location)


class Entry(Model):
    """ This is the template for an entry."""
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)

# add combined later.

    entry_date = DateTimeField()
    title = TextField()
    minutes = IntegerField()
    notes = TextField(default=None)

    class Meta:
        database = db


class DatabaseIntermediary():
    """ This class is an intermediary that adds, deletes, or changes
    the data from the database that is used for the database work log
    project. It also gets that same information from the database
    and returns it. """

    def add(self, first_name, last_name, user_date, title, minutes,
            notes=None):
            user_date = datetime.datetime.strptime(user_date, '%m/%d/%Y')
            entry = Entry()
            entry.create(first_name=first_name,
                         last_name=last_name,
                         entry_date=user_date,
                         title=title,
                         minutes=minutes,
                         notes=notes)

    def return_all(self, first_name=None, last_name=None):
        """ This gets all of the information from the database
        and returns it depending on the names given. """
        entries = Entry.select().order_by(Entry.entry_date)
        returned_list = []
        if not first_name:
            for entry in entries:
                # This creates a dictionary for each entry and adds
                # it to returned_list to return.
                dictionary = {'first_name': entry.first_name}
                dictionary['last_name'] = entry.last_name
                str_date = datetime.datetime.strftime(entry.entry_date,
                                                      '%m/%d/%Y')
                dictionary['date'] = str_date
                dictionary['title'] = entry.title
                dictionary['minutes'] = entry.minutes
                dictionary['notes'] = entry.notes
                returned_list.append(dictionary)
        return returned_list


def initialize():
    """Creates the database and an Entry is they don't exsist."""
    entry = Entry()
    db.connect()
    db.create_tables([entry], safe=True)


initialize()
