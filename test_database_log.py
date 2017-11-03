import unittest

from database_intermediary import DatabaseIntermediary


class DatabaseIntermediaryTest(unittest.TestCase):
    """ Tests the DatabaseIntermediary class."""

    def Setup(self):
        """ Sets up information for the rest of the tests. """
        pass

    def test_add(self):
        """ This tests to see if add craches. """
        # Everything added will be deleted later in test_delete.
        first_name = 'Trevor'
        last_name = 'Harvey'
        entry_date = '04/19/2012'
        title = 'Test'
        minutes = 34
        notes = 'This is testing entries.'
        data = DatabaseIntermediary()
        data.add(first_name, last_name, entry_date, title, minutes, notes)

    def test_return_all(self):
        """ This tests to see if return_all crashes. """
        data = DatabaseIntermediary()
        data.return_all()


unittest.main()
