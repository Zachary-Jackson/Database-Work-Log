import unittest

from database_intermediary import DatabaseIntermediary


class DatabaseIntermediaryTest(unittest.TestCase):
    """ Tests the DatabaseIntermediary class."""

    def test_add(self):
        """ This tests to see if add craches. """
        # Everything added will be deleted later in test_delete.
        first_name = 'Trevor'
        last_name = 'Harvey'
        entry_date = '04/19/2012'
        title = 'Test'
        minutes = 34
        notes = 'testing entries. and regex (555) 555-3425'
        data = DatabaseIntermediary()
        data.add(first_name, last_name, entry_date, title, minutes, notes)

    def test_return_all(self):
        """ This tests to see if return_all crashes. """
        data = DatabaseIntermediary()
        data.return_all()

    def test_return_all_name(self):
        """ This tests to see if return_all crashes via name search. """
        data = DatabaseIntermediary()
        data.return_all(first_name='Zach', last_name='J')

    def test_search_one_date(self):
        """ This tests to see if search crashes."""
        data = DatabaseIntermediary()
        # search via 1 date.
        data.search(user_date='04/19/2012', all_names=True)

    def test_search_two_dates(self):
        """ This tests to see if search crashes."""
        data = DatabaseIntermediary()
        # search via 2 dates.
        data.search(user_date='01/01/1800', second_date='02/04/1827',
                    all_names=True)
        data.search(user_date='5/21/2012', second_date='04/10/2012',
                    all_names=True)
        data.search(user_date='03/12/0001', second_date='03/13/0001',
                    all_names=True)

    def test_search_minutes(self):
        """ This tests to see if search crashes."""
        data = DatabaseIntermediary()
        # search via minutes.
        data.search(minutes=34, all_names=True)

    def test_search_key_phrase(self):
        """ This tests to see if search crashes."""
        data = DatabaseIntermediary()
        # search via key phrase.
        data.search(key_phrase='testing entries.', all_names=True)

    def test_search_regex(self):
        """ This tests to see if search crashes."""
        data = DatabaseIntermediary()
        # search via regex emails.
        data.search(regex='[-\w\d.+]+@[-\w\d.]+', all_names=True)
        # search via regex phone numbers
        data.search(regex='\(?\d{3}\)?-?\s?\d{3}-\d{4}', all_names=True)


unittest.main()
