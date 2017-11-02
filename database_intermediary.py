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

    entry_date = CharField(max_length=255)
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
        entry = Entry()
        entry.create(first_name=first_name,
                     last_name=last_name,
                     entry_date=user_date,
                     title=title,
                     minutes=minutes,
                     notes=notes)


def initialize():
    """Creates the database and an Entry is they don't exsist."""
    entry = Entry()
    db.connect()
    db.create_tables([entry], safe=True)


initialize()
