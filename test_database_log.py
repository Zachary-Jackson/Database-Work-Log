import datetime
import unittest

from database_intermediary import DatabaseIntermediary


class DatabaseIntermediaryTest(unittest.TestCase):
    """ Tests the DatabaseIntermediary class."""

    def test_add(self):
        """ This tests to see if add craches. Add is tested in the
        following tests becuase these two entries are searched through."""
        # Everything added will be deleted later in test_delete.
        first_name = 'Trevor'
        last_name = 'Harvey'
        entry_date = '04/19/2012'
        title = 'Test'
        minutes = 34
        notes = 'testing entries. and regex (555) 555-3425'
        data = DatabaseIntermediary()
        data.add(first_name, last_name, entry_date, title, minutes, notes)
        # second test add
        first_name = 'Nik'
        last_name = 'Silver'
        entry_date = '01/14/1827'
        title = 'random@mail.com'
        minutes = 34
        notes = 'This is an email test.'
        data = DatabaseIntermediary()
        data.add(first_name, last_name, entry_date, title, minutes, notes)

    def test_return_all(self):
        """ This tests to see if return_all crashes. """
        data = DatabaseIntermediary()
        data.return_all()

    def test_return_all_names(self):
        """ This tests to see if return_all finds Nik. """
        data = DatabaseIntermediary()
        test = data.return_all(first_name='Nik', last_name='Silver')
        self.assertEqual(test[0].first_name, 'Nik')

        test_2 = data.return_all(first_name='Trevor', last_name='Harvey')
        self.assertEqual(test_2[0].last_name, 'Harvey')

    def test_search_one_date(self):
        """ This tests to see if search finds by date."""
        data = DatabaseIntermediary()
        # search via 1 date.
        test = data.search(user_date='04/19/2012', all_names=True)
        item_date = datetime.datetime(month=4, day=19, year=2012)
        self.assertEqual(test[0].entry_date, item_date)

    def test_search_two_dates(self):
        """ This tests to see if search crashes or has the correct value."""
        data = DatabaseIntermediary()
        # search via 2 dates.
        data.search(user_date='01/01/1800', second_date='02/04/1827',
                    all_names=True)

        test = data.search(user_date='5/21/2012', second_date='04/10/2012',
                           first_name='Trevor', last_name='Harvey')
        item_date = datetime.datetime(month=4, day=19, year=2012)
        self.assertEqual(test[0].entry_date, item_date)

        data.search(user_date='1/10/2013', second_date='5/21/2011',
                    first_name='Trevor', last_name='Harvey')
        data.search(user_date='03/12/0001', second_date='03/13/0001',
                    all_names=True)

    def test_search_minutes(self):
        """ This tests to see if search finds 34."""
        data = DatabaseIntermediary()
        # search via minutes.
        test = data.search(minutes=34, all_names=True)
        self.assertEqual(test[0].minutes, 34)

    def test_search_key_phrase(self):
        """ This tests to see if search gets the correct value."""
        data = DatabaseIntermediary()
        # search via key phrase.
        test = data.search(key_phrase='testing entries.', all_names=True)
        self.assertIn('testing entries.', test[0].notes)

    def test_search_regex(self):
        """ This tests to see if search crashes."""
        data = DatabaseIntermediary()
        # search via regex emails.
        test = data.search(regex='[-\w\d.+]+@[-\w\d.]+', all_names=True)
        self.assertIn('random@mail.com', test[0].title)
        # search via regex phone numbers
        test_2 = data.search(regex='\(?\d{3}\)?-?\s?\d{3}-\d{4}',
                             all_names=True)
        self.assertIn('(555) 555-3425', test_2[0].notes)

    def test_name_returner(self):
        """ This tests to see if we get Trevor harvey and Nik Silver."""
        data = DatabaseIntermediary()
        test = data.name_returner()
        self.assertIn(('Trevor', 'Harvey'), test)
        self.assertIn(('Nik', 'Silver'), test)


unittest.main()
