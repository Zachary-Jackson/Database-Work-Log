import datetime
import unittest


from entry_changer import EntryChanger
from database_intermediary import DatabaseIntermediary
import database_work_log


class EntryChangerTest(unittest.TestCase):
    """ Tests the EntryChanger class."""
    def setup(self):
        # ec stands for EntryChanger
        self.ec = EntryChanger()


class DatabaseIntermediaryTest(unittest.TestCase):
    """ Tests the DatabaseIntermediary class."""
    def setUp(self):
        self.data = DatabaseIntermediary()

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
        self.data.add(first_name, last_name, entry_date, title, minutes, notes)
        # second test add
        first_name = 'Nik'
        last_name = 'Silver'
        entry_date = '01/14/1827'
        title = 'random@mail.com'
        minutes = 34
        notes = 'This is an email test.'

        self.data.add(first_name, last_name, entry_date, title, minutes, notes)

    def test_return_all(self):
        """ This tests to see if return_all crashes. """
        self.data.return_all()

    def test_return_all_names(self):
        """ This tests to see if return_all finds Nik. """
        test = self.data.return_all(first_name='Nik', last_name='Silver')
        self.assertEqual(test[0].first_name, 'Nik')

        test_2 = self.data.return_all(first_name='Trevor', last_name='Harvey')
        self.assertEqual(test_2[0].last_name, 'Harvey')

    def test_search_one_date(self):
        """ This tests to see if search finds by date."""
        # search via 1 date.
        test = self.data.search(user_date='04/19/2012', all_names=True)
        item_date = datetime.datetime(month=4, day=19, year=2012)
        self.assertEqual(test[0].entry_date, item_date)

    def test_search_two_dates(self):
        """ This tests to see if search crashes or has the correct value."""
        # search via 2 dates.
        self.data.search(user_date='01/01/1800', second_date='02/04/1827',
                         all_names=True)

        test = self.data.search(user_date='5/21/2012',
                                second_date='04/10/2012', first_name='Trevor',
                                last_name='Harvey')
        item_date = datetime.datetime(month=4, day=19, year=2012)
        self.assertEqual(test[0].entry_date, item_date)

        self.data.search(user_date='03/12/0001', second_date='03/13/0001',
                         all_names=True)
        return self.data.search(user_date='1/10/2013', second_date='5/21/2011',
                                first_name='Trevor', last_name='Harvey')

    def test_search_minutes(self):
        """ This tests to see if search finds 34."""
        # search via minutes.
        test = self.data.search(minutes=34, all_names=True)
        self.assertEqual(test[0].minutes, 34)

    def test_search_key_phrase(self):
        """ This tests to see if search gets the correct value."""
        # search via key phrase.
        test = self.data.search(key_phrase='testing entries.', all_names=True)
        self.assertIn('testing entries.', test[0].notes)

    def test_search_regex(self):
        """ This tests to see if search crashes."""
        # search via regex emails.
        test = self.data.search(regex='[-\w\d.+]+@[-\w\d.]+', all_names=True)
        self.assertIn('random@mail.com', test[0].title)
        # search via regex phone numbers
        test_2 = self.data.search(regex='\(?\d{3}\)?-?\s?\d{3}-\d{4}',
                                  all_names=True)
        self.assertIn('(555) 555-3425', test_2[0].notes)

    def test_name_returner(self):
        """ This tests to see if we get Trevor harvey and Nik Silver."""
        test = self.data.name_returner()
        self.assertIn(('Trevor', 'Harvey'), test)
        self.assertIn(('Nik', 'Silver'), test)

    class Database_work_log_test(unittest.TestCase):
        pass


if __name__ == '__main__':
    unittest.main()
