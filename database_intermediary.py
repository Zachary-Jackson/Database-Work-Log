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
        elif not all_names:
            self.return_all(first_name, last_name)
            db_contents = self.db_contents

        # This starts the area where there are a bunch of if statments
        # to check which kind of search the user is preforming.
        # Search by date, minutes, key_phrase, or regex.
        returned_list = []

        if user_date and not second_date:
            for item in db_contents:
                item_date = datetime.datetime.strftime(item.entry_date,
                                                       '%m/%d/%Y')
                if user_date == item_date:
                    returned_list.append(item)

        if user_date and second_date:
            user_date = datetime.datetime.strptime(user_date, '%m/%d/%Y')
            second_date = datetime.datetime.strptime(second_date, '%m/%d/%Y')
            # This determines the order of date_1 and date_2
            if user_date <= second_date:
                date_1_first = True
            else:
                date_1_first = False
            for item in db_contents:
                if date_1_first:
                    if (user_date <= item.entry_date and second_date
                            >= item.entry_date):
                        returned_list.append(item)
                else:
                    if (second_date <= item.entry_date and user_date >=
                            item.entry_date):
                        returned_list.append(item)

        elif minutes:
            # searching by the minutes section in the dictionary prevents
            # minutes from catching dates.
            for item in db_contents:
                if minutes == item.minutes:
                    returned_list.append(item)

        elif key_phrase:
            for item in db_contents:
                if key_phrase == str(item.first_name) or \
                        key_phrase == str(item.last_name) or \
                        key_phrase in str(item.entry_date) or \
                        key_phrase in str(item.title) or \
                        key_phrase in str(item.minutes) or \
                        key_phrase in str(item.notes):
                    returned_list.append(item)

        elif regex:
            # This converts each dictionary for regex patterns in
            # the keys of 'title' and 'notes'
            for item in db_contents:
                if re.findall(r'{}'.format(regex), item.title):
                    returned_list.append(item)
                elif re.findall(r'{}'.format(regex), item.notes):
                    returned_list.append(item)
        self.found = returned_list
        return returned_list

    def editor(self, old_item, n_first=None, n_last=None, n_entry_date=None,
               n_title=None, n_minutes=None, n_notes=None, edit=False):
        """ This deletes an item that is sent into the editor if it
        correlates to an item in the database. If edit is True it adds
        one in its place."""
        # This possibly refreshes the database contents.
        self.return_all
        for item in self.db_contents:
            if old_item.first_name == item.first_name and\
               old_item.last_name == item.last_name and\
               old_item.entry_date == item.entry_date and\
               old_item.title == item.title and\
               old_item.minutes == item.minutes and\
               old_item.notes == item.notes:
                item.delete_instance()
        if edit:
            self.add(n_first, n_last, n_entry_date, n_title, n_minutes,
                     n_notes)

    def return_all(self, first_name=False, last_name=False):
        """ This gets all of the information from the database
        and returns it depending on the names given. """
        entries = Entry.select().order_by(Entry.entry_date)
        returned_list = []
        # This creates a dictionary for each entry and adds
        # it to returned_list to return.
        if first_name:
            for entry in entries:
                if entry.first_name == first_name and \
                        entry.last_name == last_name:
                    returned_list.append(entry)
        elif not first_name:
            for entry in entries:
                returned_list.append(entry)
        self.db_contents = returned_list
        return returned_list

    def name_returner(self):
        """ This finds all of the names that are currently in the database."""
        entry_list = self.return_all()
        returned_list = []
        for item in entry_list:
            name = (item.first_name, item.last_name)
            if name not in returned_list:
                returned_list.append(name)
        returned_list.sort()
        return returned_list


def initialize():
    """Creates the database and an Entry is they don't exsist."""
    entry = Entry()
    db.connect()
    db.create_tables([entry], safe=True)


initialize()
