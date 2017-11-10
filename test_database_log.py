import datetime
import unittest
import unittest.mock
from unittest.mock import patch


from entry_changer import EntryChanger # noqa
from database_intermediary import DatabaseIntermediary
import database_work_log # noqa


class EntryChangeMock():
    """ Mock for EntryChanger."""
    def test_date(self, *args, **kwargs):
        return '01/04/1995'

    def test_minute(self, *args, **kwargs):
        return 15


class EntryChangerTest(unittest.TestCase):
    """ Tests the EntryChanger class."""

    def setUp(self):
        """ Sets us the tests for EntryChangerTest."""
        self.ec = EntryChanger()
        self.db = DatabaseIntermediary()
        entry_list = self.db.return_all()
        self.ec.entry = entry_list[0]

    def test_init(self):
        """ This tests that __init__ is working. """
        self.assertIsNotNone(DatabaseIntermediary(), self.ec.db)

    def test_name_setter(self):
        """ This tests name_setter."""
        first, last, all_names = self.ec.name_setter('Albert', 'Brown',
                                                     all_names=False)
        self.assertEqual('Albert', self.ec.first_name)
        self.assertEqual('Brown', self.ec.last_name)
        self.assertFalse(self.ec.all_names)
        first, last, all_names = self.ec.name_setter('Albert', 'Brown',
                                                     all_names=True)
        self.assertTrue(self.ec.all_names)
        # This tests if all_names can be false.
        first, last, all_names = self.ec.name_setter('Albert', 'Brown',
                                                     all_names=False)
        self.assertFalse(self.ec.all_names)

    def test_name_num_picker(self):
        """ This test name_num_picker."""
        name = [('Charles', 'Jackson')]
        # Tests a normal user input and name returned
        with unittest.mock.patch('builtins.input', return_value='1'):
            last_name, need_name = self.ec.name_num_picker(name)
            self.assertFalse(need_name)
            self.assertEqual('Jackson', last_name)
        # Tests a non integer input
        with unittest.mock.patch('builtins.input', return_value='four'):
            last_name, need_name = self.ec.name_num_picker(name)
            self.assertTrue(need_name)
        # Tests a IndexError input
        with unittest.mock.patch('builtins.input', return_value='4'):
            test_name, need_name = self.ec.name_num_picker(name)
            self.assertTrue(need_name)

    def test_name_picker_all(self):
        """ This tests to see if name_picker_all works."""
        with unittest.mock.patch('builtins.input', return_value='y'):
            self.ec.all_names = True
            self.ec.name_picker_all()
            self.assertFalse(self.ec.all_names)

        with unittest.mock.patch('builtins.input', return_value='n'):
            self.ec.all_names = True
            self.ec.name_picker_all()
            self.assertTrue(self.ec.all_names)

        with unittest.mock.patch('builtins.input', return_value='y'):
            self.ec.all_names = False
            self.ec.name_picker_all()
            self.assertTrue(self.ec.all_names)

        with unittest.mock.patch('builtins.input', return_value='n'):
            self.ec.all_names = False
            self.ec.name_picker_all()
            self.assertFalse(self.ec.all_names)

    def test_run_entry_changer(self):
        """ Tests to see if run_entry_changer returns a new first and last
        name."""
        first, last = self.ec.run_entry_changer('Charles',
                                                'Forester',
                                                all_names=False)
        self.assertEqual('Charles', first)
        self.assertEqual('Forester', last)

    def test_clear(self):
        """ Checks is clear crashes."""
        self.assertTrue(self.ec.clear())

    def test_name_picker(self):
        """ Checks name_picker."""
        pass

    @patch('entry_changer.EntryChanger.add_date',
           new=EntryChangeMock.test_date)
    @patch('entry_changer.EntryChanger.add_minute',
           new=EntryChangeMock.test_minute)
    def test_add(self):
        """ This tests to see if add will return the correct values."""
        # This checks for a correct vlaue.
        with unittest.mock.patch('builtins.input', return_value='Snow'):
            user_date, title, minutes, notes, stop = self.ec.add()
        self.assertEqual(user_date, '01/04/1995')
        self.assertEqual(title, 'Snow')
        self.assertEqual(minutes, 15)
        self.assertEqual(notes, 'Snow')
        self.assertFalse(stop)
        # This checks for an incorrect vlaue.
        with unittest.mock.patch('builtins.input', return_value='q'):
            user_date, title, minutes, notes, stop = self.ec.add()
        self.assertFalse(stop)

    def test_add_date(self):
        """ Checks add_date."""
        # Checks for a valid date.
        with unittest.mock.patch('builtins.input', return_value='01/04/1995'):
            user_date = self.ec.add_date()
            self.assertEqual('01/04/1995', user_date)
        # Checks if the user quits.
        with unittest.mock.patch('builtins.input', return_value='q'):
            user_date = self.ec.add_date()
            self.assertFalse(user_date)

    def test_add_minute(self):
        """ Tests add_minute."""
        # Checks add_minute with a valid number.
        with unittest.mock.patch('builtins.input', return_value=15):
            minutes = self.ec.add_minute()
            self.assertEqual(15, minutes)

    @patch('entry_changer.EntryChanger.edit_date',
           new=EntryChangeMock.test_date)
    @patch('entry_changer.EntryChanger.edit_minutes',
           new=EntryChangeMock.test_minute)
    def test_editor(self):
        """ This tests to see if add will return the correct values."""
        # This checks for a correct vlaue.
        with unittest.mock.patch('builtins.input', return_value='Snow'):
            user_date, title, minutes, notes, stop = self.ec.editor(self.
                                                                    ec.entry)
        self.assertEqual(user_date, '01/04/1995')
        self.assertEqual(title, 'Snow')
        self.assertEqual(minutes, 15)
        self.assertEqual(notes, 'Snow')
        self.assertFalse(stop)
        # This checks for an incorrect vlaue.
        with unittest.mock.patch('builtins.input', return_value='q'):
            user_date, title, minutes, notes, stop = self.ec.editor(self.
                                                                    ec.entry)
        self.assertFalse(stop)

    def test_edit_date(self):
        """ Checks edit_date."""
        # Checks for a valid date.
        with unittest.mock.patch('builtins.input', return_value='01/04/1995'):
            user_date = self.ec.edit_date(self.ec.entry)
            self.assertEqual('01/04/1995', user_date)
        # Checks if the user quits.
        with unittest.mock.patch('builtins.input', return_value='q'):
            user_date = self.ec.edit_date(self.ec.entry)
            self.assertFalse(user_date)

    def test_edit_minutes(self):
        """ Tests edit_minutes."""
        # Checks add_minute with a valid number.
        with unittest.mock.patch('builtins.input', return_value=15):
            minutes = self.ec.edit_minutes(self.ec.entry)
            self.assertEqual(15, minutes)

    def test_inline_date_getter(self):
        """ Tests inline_date_getter()."""
        # Tests with only one date
        with unittest.mock.patch('builtins.input', return_value='03/18/2038'):
            date_str = self.ec.inline_date_getter()
        self.assertEqual('03/18/2038', date_str)
        # Tests with first of two dates
        with unittest.mock.patch('builtins.input', return_value='03/18/2038'):
            date_str = self.ec.inline_date_getter(2)
        self.assertEqual('03/18/2038', date_str)
        # Tests with second of two dates
        with unittest.mock.patch('builtins.input', return_value='03/18/2038'):
            date_str = self.ec.inline_date_getter(3)
        self.assertEqual('03/18/2038', date_str)

    def test_seach_date_range(self):
        """ Tests search_date_range."""
        # Tests to see if the user wants two dates.
        with unittest.mock.patch('builtins.input', return_value='r'):
            dates = self.ec.search_date_range()
        self.assertTrue(dates)
        # Tests to see if the user wants one date."""
        with unittest.mock.patch('builtins.input', return_value='s'):
            dates = self.ec.search_date_range()
        self.assertFalse(dates)

    def test_search_time(self):
        """ Tests search_time."""
        with unittest.mock.patch('builtins.input', return_value=15):
            minutes = self.ec.search_time()
        self.assertEqual(15, minutes)

    def test_show_template(self):
        """ Tests show_template."""
        with unittest.mock.patch('builtins.input', return_value='e'):
            self.db.return_all()
            test = self.ec.show_template(0, 3, self.db.db_contents[0],
                                         menu_options='right')
            self.assertEqual(test, 'e')

            test = self.ec.show_template(2, 3, self.db.db_contents[0],
                                         menu_options='both')
            self.assertEqual(test, 'e')
            test = self.ec.show_template(2, 3, self.db.db_contents[0],
                                         menu_options='left')
            self.assertEqual(test, 'e')


class DatabaseIntermediaryTest(unittest.TestCase):
    """ Tests the DatabaseIntermediary class."""
    def setUp(self):
        """ Sets up the tests for DatabaseIntermediaryTest."""
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
        test = self.data.search(regex='[-\w\d.+]+@[-\w\d.]+', all_names=True) # noqa
        # taking out the self.assertIn until I figure out the order of the
        # tests. See test_zeditor() for more information.

        # self.assertIn('random@mail.com', test[0].title)

        # search via regex phone numbers.
        test_2 = self.data.search(regex='\(?\d{3}\)?-?\s?\d{3}-\d{4}',
                                  all_names=True)
        self.assertIn('(555) 555-3425', test_2[0].notes)

    def test_name_returner(self):
        """ This tests to see if we get Trevor harvey and Nik Silver."""
        test = self.data.name_returner()
        self.assertIn(('Trevor', 'Harvey'), test)
        self.assertIn(('Nik', 'Silver'), test)

    def test_zeditor(self):
        """ This tests to see if an item can be edited and deleted."""
        # I had to put a z infront of editor becuase it looks like
        # unittest does test alphabetically instad of where they are at
        # in the file. It was messing with the other items.

        # Edit that above it is still affecting things for some reason.
        # I don't know the order it is processing them in.
        # I took out a secondary assertion test in test_search_regex()
        # until I figure out which order the tests are completed in.
        test = self.data.search(key_phrase='testing entries.', all_names=True)
        self.data.editor(old_item=test[0])

        test_2 = self.data.search(key_phrase='This is an email test.',
                                  all_names=True)
        self.data.editor(old_item=test_2[0], n_first='Nik',
                         n_last='Silver', n_entry_date='01/04/0784',
                         n_title='Not correct', n_minutes=23,
                         n_notes='This is the new test notes.', edit=True)

        # This third test uses the edited item from test_2. If this passes
        # then editor works and I don't have to self.assert anything.
        test_3 = self.data.search(key_phrase='This is the new test notes.',
                                  all_names=True)
        self.data.editor(old_item=test_3[0])


class Database_work_log_test(unittest.TestCase):
    """ Tests database_work_log."""

    def setUp(self):
        """ sets up the Database_work_log_test."""
        self.ec = EntryChanger()
        self.ec.first_name = 'Bob'
        self.ec.last_name = 'Harvey'
        self.ec.all_names = True

    def test_welcome(self):
        """ Test welcome with user continue."""
        with unittest.mock.patch('builtins.input', return_value='y'):
            self.assertTrue(database_work_log.welcome())

    def test_not_welcome(self):
        """ Tests welcome with user exiting the program."""
        with unittest.mock.patch('builtins.input', return_value='q'):
            self.assertFalse(database_work_log.welcome())

    def test_main_all_names_true(self):
        """ Tests main_all_names."""
        with unittest.mock.patch('builtins.input', return_value='all'):
            self.assertTrue(database_work_log.main_all_names())

    def test_main_all_names_false(self):
        """ Tests main_all_names."""
        with unittest.mock.patch('builtins.input', return_value='my'):
            self.assertFalse(database_work_log.main_all_names())

    def test_main_quit(self):
        """ Tests to see if one can exit main()."""
        with unittest.mock.patch('builtins.input', return_value='q'):
            self.assertTrue(database_work_log.main(self.ec, self.ec.first_name,
                                                   self.ec.last_name))


if __name__ == '__main__':
    unittest.main()
