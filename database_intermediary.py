import datetime
import os
import re

from peewee import * # noqa

current_location = os.path.dirname(os.path.abspath(__file__))
file_location = os.path.join(current_location, 'database.db')
# noqa, is added after peewee related lines so it does not give a
# flake8 error.
db = SqliteDatabase(file_location) # noqa


class Entry(Model): # noqa
    """ This is the template for an entry."""
    first_name = CharField(max_length=255) # noqa
    last_name = CharField(max_length=255) # noqa

# add combined later.

    entry_date = DateTimeField() # noqa
    title = TextField() # noqa
    minutes = IntegerField() # noqa
    notes = TextField(default=None) # noqa

    class Meta:
        database = db


class DatabaseIntermediary():
    """ This class is an intermediary that adds, deletes, or changes
    the data from the database that is used for the database work log
    project. It also gets that same information from the database
    and returns it. """

    def add(self, first_name, last_name, user_date, title, minutes,
            notes=None):
            """ This adds an Entry to the database. """
            user_date = datetime.datetime.strptime(user_date, '%m/%d/%Y')
            entry = Entry()
            entry.create(first_name=first_name,
                         last_name=last_name,
                         entry_date=user_date,
                         title=title,
                         minutes=minutes,
                         notes=notes)

    def search(self, user_date=None, second_date=None, minutes=None,
               key_phrase=None, regex=None, first_name=None,
               last_name=None, all_names=False, *args, **kwargs):
        """ This takes any of the variables above and searches the Database
        using the paramiters given above. """
        # This gets the contents of the database depending on if
        # the user is searching by all or one name.
        if all_names:
            self.return_all()
            db_contents = self.db_contents
        else:
            self.return_all(first_name, last_name)
            db_contents = self.db_contents

        # This starts the area where there are a bunch of if statments
        # to check which kind of search the user is preforming.
        # Search by date, minutes, key_phrase, or regex.
        returned_list = []

        if user_date and not second_date:
            for item in db_contents:
                if user_date == item['date']:
                    returned_list.append(item)

        if user_date and second_date:
            # This determines the order of date_1 and date_2
            if user_date <= second_date:
                date_1_first = True
            else:
                date_1_first = False
            for item in db_contents:
                if date_1_first:
                    if (user_date <= item['date'] and second_date
                            >= item['date']):
                        returned_list.append(item)
                else:
                    if (second_date <= item['date'] and user_date >=
                            item['date']):
                        returned_list.append(item)

        elif minutes:
            # searching by the minutes section in the dictionary prevents
            # minutes from catching dates.
            for item in db_contents:
                if minutes == item['minutes']:
                    returned_list.append(item)

        elif key_phrase:
            for item in db_contents:
                # This changes item['minutes'] to a string so it can be
                # searched through.
                item['minutes'] = str(item['minutes'])
                for value in item.values():
                    if key_phrase in value:
                        returned_list.append(item)
                        break

        elif regex:
            # This converts each dictionary for regex patterns in
            # the keys of 'title' and 'notes'
            for item in db_contents:
                if re.findall(r'{}'.format(regex), item['title']):
                    returned_list.append(item)
                elif re.findall(r'{}'.format(regex), item['notes']):
                    returned_list.append(item)
        self.found = returned_list
        return self.found

    def return_all(self, first_name=False, last_name=False):
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
        else:
            for entry in entries:
                # This creates a dictionary for each entry and adds
                # it to returned_list to return.
                if entry.first_name == first_name and \
                   entry.last_name == last_name:
                    dictionary = {'first_name': entry.first_name}
                    dictionary['last_name'] = entry.last_name
                    str_date = datetime.datetime.strftime(entry.entry_date,
                                                          '%m/%d/%Y')
                    dictionary['date'] = str_date
                    dictionary['title'] = entry.title
                    dictionary['minutes'] = entry.minutes
                    dictionary['notes'] = entry.notes
                    returned_list.append(dictionary)
        self.db_contents = returned_list
        return returned_list


def initialize():
    """Creates the database and an Entry is they don't exsist."""
    entry = Entry()
    db.connect()
    db.create_tables([entry], safe=True)


initialize()
