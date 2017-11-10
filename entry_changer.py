import datetime
import os
import time

from database_intermediary import DatabaseIntermediary


class EntryChanger():
    """ This class handles the menu and logic work for database_work_log.py.
    The user imput is sent into the DatabaseIntermediary class to be
    processed into the database file. """

    def __init__(self):
        """ This initalizes EntryChanger."""
        self.db = DatabaseIntermediary()
        self.first_name = ''
        self.last_name = ''
        self.all_names = True

    def name_setter(self, first_name=None, last_name=None, all_names=None):
        """ This sets the first name, last name, and if all names are used."""
        if first_name:
            self.first_name = first_name
            self.last_name = last_name
        if all_names:
            self.all_names = True
        elif all_names is False:
            self.all_names = False
        return self.first_name, self.last_name, self.all_names

    def run_entry_changer(self, first_name=None, last_name=None, command=None,
                          all_names=False):
        """ This is responsible for controling which method entry_changer is
        started off with. It is also responsible for returning any possible
        changes in the first and last name sence entry_changer has been
        run"""
        self.name_setter(first_name, last_name, all_names)
        # This controls which method entry_changer is started with.
        if command == 'add':
            user_date, title, minutes, notes, stop = self.add()
            if not stop:
                self.db.add(self.first_name, self.last_name,
                            user_date=user_date,
                            title=title, minutes=minutes, notes=notes)
        if command == 'show all':
            self.show_all()
        if command == 'search':
            self.search()
        if command == 'get names':
            self.name_picker()
        # This returns the names to database_work_log incase the user exits
        # to the main menu, but wants to continue.
        return self.first_name, self.last_name

    def clear(self):
        """ This clears the screen for easier viewing. """
        os.system('cls' if os.name == 'nt' else 'clear')
        return True

    def name_picker_all(self):
        """ This choices if the user wants to search by one or all names. """
        self.clear()
        if self.all_names:
            all_names = input("\n  Do you want to search by a single name? " +
                              "Y/n").lower()
            if all_names != 'n':
                self.all_names = False
                self.name_picker()
        else:
            all_names = input("\n  Do you want to search by all names? " +
                              "Y/n").lower()
            if all_names != 'n':
                self.all_names = True

    def name_num_picker(self, found_names):
        """ This gets the user's chosen input if they want to
        choice a number. It returns the name and need_last_name."""
        last_name = ''
        if found_names:
            self.clear()
            print('  Please enter the number of the name you ' +
                  'want to use.\n' +
                  '  Or enter anything else to continue.\n')
            name_counter = 1
            for name in found_names:
                print(('  {}.  {} {}.  '.format(name_counter,
                      name[0], name[1])))
                name_counter += 1
            use = input('  ')
            # Tries to correlate the int() version of use into a
            # number if possible.
            try:
                use = int(use)
            except ValueError:
                need_last_name = True
                return last_name, need_last_name
            else:
                try:
                    last_name = found_names[use-1][1]
                except IndexError:
                    need_last_name = True
                    return last_name, need_last_name
                else:
                    need_last_name = False
                    return last_name, need_last_name
        else:
            need_last_name = True
            return last_name, need_last_name

    def name_picker(self):
        """ This gathers a single users first and last name. """
        while True:
            clear_screen = True
            while True:
                if clear_screen:
                    self.clear()
                    names = self.db.name_returner()
                    self.clear()
                    # name_counter choses if a name is displayed beside another
                    name_number = 0
                    name_counter = 0
                    if len(names) < 12:
                        print('\n    Here are the current users to the Work ' +
                              'Log Program.\n')
                        for name in names:
                            if name_counter == 0:
                                print("  {} {}".format(name[0], name[1]),
                                      end='')
                                name_counter += 1
                            else:
                                if name_counter == 3:
                                    print(', {} {}'.format(name[0], name[1]))
                                    name_counter = 0
                                else:
                                    print(', {} {}'.format(name[0], name[1]),
                                          end='')
                                    name_counter += 1
                            name_number += 1
                    print('')

                first_name = input("\n  Please enter a first name.  \n  ")\
                    .title().strip()

                # found_names is used a couple lines down.
                found_names = []

                if ' ' in first_name or first_name == '':
                    clear_screen = False
                else:
                    # Checks to see if the first_name entered by the user
                    # has a corresponding last name.
                    found_names = []
                    for name in names:
                        if first_name in name[0]:
                            found_names.append(name)

                last_name, need_last_name = self.name_num_picker(found_names)
                break

            clear_screen = False
            while need_last_name:
                if clear_screen:
                    for _ in range(3, 0, -1):
                        self.clear()
                        print("\n  Please enter a last name with no " +
                              "middle names.\n")
                        print("  You can enter another name in {} seconds"
                              .format(_))
                        time.sleep(1)
                        self.clear()
                last_name = input("\n  Please enter a last name.  \n  ")\
                    .title().strip()
                if ' ' in last_name or last_name == '':
                    clear_screen = True
                else:
                    break

            good_name = input("\n  Is {} {} the name you want to use? Y/n  "
                              .format(first_name, last_name)).lower()
            if good_name != 'n':
                self.name_setter(first_name, last_name)
                return self.first_name, self.last_name
                break

    def add(self):
        """ This gathers information from the user and sends it to
        DatabaseIntermediary() to be stored into the database file."""
        # Gets the potential user date from the user.
        user_date = self.add_date()
        if not user_date:
            return '', '', '', '', True

        # If the user exited out of self.add_date() this does not run.
        # Collects the event title
        title = input("\n  Please enter a title for the work log.  ")
        # Gets the minutes form the user.
        minutes = self.add_minute()
        # Gathers the information associated with the tasks
        notes = input("\n  Enter any notes you want about the task.\n" +
                      "  This section is optional.  ")
        stop = False
        return user_date, title, minutes, notes, stop

    def add_date(self):
        """ Returns a date to add() or False."""
        valid_variable = True
        # Collects the date
        while True:
            self.clear()
            if valid_variable is False:
                print("\n    That is not a valid date." +
                      "  Please enter a valid one.\n")
            user_date = input("\n    Please enter the date in " +
                              "  MM/DD/YYYY format.\n" +
                              "  Enter 'q' to return to the main menu.  ")
            try:
                datetime.datetime.strptime(user_date, '%m/%d/%Y')
            except ValueError:
                if user_date == 'q' or user_date == 'quit':
                    return False
                else:
                    valid_variable = False
                    continue
            else:
                return user_date

    def add_minute(self):
        """ This gets an answer from the user and returns minutes to
        add()."""
        # Collects the minutes spent on tasks
        valid_variable = True
        while True:
            if valid_variable is False:
                self.clear()
                print("\n  That is not a valid number for minutes.\n" +
                      "  Please enter a number like '15'.")
            try:
                minutes = int(input("\n  Please enter the minutes spent " +
                                    "on the task.  "))
            except ValueError:
                valid_variable = False
            else:
                return minutes

    def editor(self, old_item):
        """ This gathers information from the user and sends it to
        DatabaseIntermediary() to be stored into the database file.
        This one differs from add() only because it shows the user
        the data that is to be edited."""
        # Gets the potential user date from the user.
        user_date = self.edit_date()
        if not user_date:
            return '', '', '', '', True

        # If the user exited out of self.add_date() this does not run.
        # Collects the event title
        title = input("\n  Please enter a title for the work log.\n" +
                      "  Current title is :{}\n  ".format(old_item.title))
        # Gets the minutes variable from edit_minutes().
        minutes = self.edit_minutes(old_item)
        # Gathers the information associated with the tasks
        notes = input("\n  Enter any notes you want about the task.\n" +
                      "  Current notes are :{} \n"
                      "  This section is optional.\n  ".format(
                        old_item.notes))
        stop = False
        # This returns to new user information so it can be used to edit
        # what is given to show.
        return user_date, title, minutes, notes, stop
        # This sends all of the information to DatabaseIntermediary for
        # further processing
        self.db.editor(old_item, n_first=old_item.first_name,
                       n_last=old_item.last_name,
                       n_entry_date=user_date, n_title=title,
                       n_minutes=minutes, n_notes=notes, edit=True)
        # This returns to new user information so it can be used to edit
        # what is given to show.

    def edit_date(self, old_item):
        """ This gets a date for editor() or returns False."""
        valid_variable = True
        # Collects the date
        while True:
            entry_date = datetime.datetime.strftime(old_item.entry_date,
                                                    '%m/%d/%Y')
            self.clear()
            if valid_variable is False:
                print("\n    That is not a valid date." +
                      "  Please enter a valid one.\n")
            user_date = input("\n    Please enter the date in " +
                              "  MM/DD/YYYY format.\n" +
                              "  Current date is {}.\n".format(entry_date) +
                              "  Enter 'q' to return to the main menu.\n  ")
            try:
                datetime.datetime.strptime(user_date, '%m/%d/%Y')
            except ValueError:
                if user_date == 'q' or user_date == 'quit':
                    return False
                else:
                    valid_variable = False
                    continue
            else:
                return user_date

    def edit_minutes(self, old_item):
        """ Gets a minute value and returns it to editor()."""
        # Collects the minutes spent on tasks
        valid_variable = True
        while True:
            if valid_variable is False:
                self.clear()
                print("\n  That is not a valid number for minutes.\n" +
                      "  Please enter a number like '15'.")
            try:
                minutes = int(input("\n  Please enter the minutes spent " +
                                    "on the task.  \n" +
                                    "  Current minutes is {}\n  ".format(
                                      old_item.minutes)))
            except ValueError:
                valid_variable = False
            else:
                return minutes

    def show_all(self):
        """ This gets all of the work log entries from DatabaseIntermediary
        and sends it to self.show()."""
        # self.found_results is a dictionary with the keys of first_name,
        # last_name, date, title, minutes, and notes.
        if self.all_names:
            self.found_results = self.db.return_all()
        else:
            self.found_results = self.db.return_all(self.first_name,
                                                    self.last_name)
        self.show()

    def search(self):
        """ This gathers the users input and determins how to process the
        data using DatabaseIntermediary and sends it to self.show()."""

        # Shows the user a menu of items to choice from.
        menu_selector = self.search_main()

        # Finds by date
        if menu_selector == 'a' or menu_selector == 'a)' \
                or menu_selector == 'date':
            self.found_results = self.search_date()

        # Find by time spent
        if menu_selector == 'b' or menu_selector == 'b)' \
                or menu_selector == 'time':
            minutes = self.search_time()
            self.found_results = self.db.search(minutes=minutes)

        # Find by an exact search
        if menu_selector == 'c' or menu_selector == 'c)' \
           or menu_selector == 'exact':
            self.clear()
            key_phrase = input("  Enter the 'exact' phrase you want to " +
                               'search for.\n' +
                               '  This searches titles and notes.  ')
            self.found_results = self.db.search(key_phrase=key_phrase)

        # Find by a regular expression pattern.
        if menu_selector == 'd' or menu_selector == 'd' \
           or menu_selector == 'regular' \
           or menu_selector == 'regular expression':
            regex = input('\n  Enter the python regular expression ' +
                          'string you want to search with.  ')
            self.found_results = self.db.search(regex=regex)

        # This returns all work log items and sends them to show.
        if menu_selector == 'e' or menu_selector == 'e)' \
                or menu_selector == 'all':
            self.show_all()

        # This goes to the show method to show the user there results.
        if menu_selector != 'q' and menu_selector != 'quit' \
                and menu_selector != 'e' and menu_selector != 'e)' \
                and menu_selector != 'all':
            self.show()

    def search_main(self):
        """ This is the main menu section of search. This returns the user's
        desired outcome. It returns False if they exit."""
        # Shows the user a menu of items to choice from.
        continue_loop = True
        while continue_loop:
            self.clear()
            menu_options = ['a', 'a)', 'b', 'b)', 'c', 'c)', 'd',
                            'd)', 'e', 'e)', 'all', 'date', 'time',
                            'exact', 'regular', 'regular expression']
            exit_options = ['q', 'quit']

            if self.all_names:
                print('\n    You are currently searching by all names.')
            else:
                print("\n    You are only searching {} {}'s work logs."
                      .format(self.first_name, self.last_name))
            menu_selector = input("\n  Enter how you would like to search " +
                                  "the work log database.\n\n" +
                                  '  a) Search by date.\n' +
                                  '  b) Search by time spent\n' +
                                  '  c) Search by an exact search\n' +
                                  '  d) Search by a python ' +
                                  'regular expression\n' +
                                  '  e) Shows all work logs.\n' +
                                  '  f) Change the names to be searched.'
                                  "\n     Enter 'q' to return to the" +
                                  " main menu.  "
                                  ).lower()
            if menu_selector == 'f' or menu_selector == 'f)' or \
               menu_selector == 'change':
                self.name_picker_all()
            if menu_selector in menu_options:
                return menu_selector
            if menu_selector in exit_options:
                return False

    def inline_date_getter(self, date_number=None):
        """ This takes date_number which is an optional variable
        that tells the function which date number we are getting. """
        # This controls which string is shown to the user.
        if date_number == 1:
            string = ('\n  Please enter the first date in ' +
                      'MM/DD/YYYY format.  ')
        elif date_number == 2:
            string = ('\n  Please enter the second date in ' +
                      'MM/DD/YYYY format.  ')
        else:
            string = ('\n  Please enter the date in MM/DD/YYYY format'
                      '.  ')
        valid_variable = True
        while True:
            self.clear()
            if valid_variable is False:
                print('  That is not a valid date. Please enter a' +
                      ' valid one.\n')
            user_date = input(string)
            try:
                datetime.datetime.strptime(user_date, '%m/%d/%Y')
            except ValueError:
                valid_variable = False
                continue
            else:
                return user_date

    def search_date_range(self):
        """ This checks if the user is searching by one or two dates."""
        # This controls if the user is searching via a range of dates
        # or one date.
        while True:
            self.clear()
            dates = input("\n    Are you searching via a range of dates " +
                          " or by a single date?\n" +
                          "  Enter 'r' for a range of dates or 's' for " +
                          "single.  ")
            if dates == 'r' or dates == 'range':
                dates = True
                return dates
            elif dates == 's' or dates == 'single':
                dates = False
                return dates

    def search_date(self):
        """ This gathers the user's date prefrences and returns it to
        search()."""
        # This checks to see if the user wants one or two dates.
        dates = self.search_date_range()

        if dates:
            user_date = self.inline_date_getter(date_number=1)
            user_date_2 = self.inline_date_getter(date_number=2)
            return self.db.search(user_date=user_date, second_date=user_date_2,
                                                 first_name= # noqa
                                                 self.first_name, # noqa
                                                 last_name= # noqa
                                                 self.last_name, # noqa
                                                 all_names= # noqa
                                                 self.all_names) # noqa
        else:
            user_date = self.inline_date_getter()
            return self.db.search(user_date=user_date,
                                    first_name=self.first_name,
                                                 last_name= # noqa
                                                 self.last_name, # noqa
                                                 all_names = # noqa
                                                 self.all_names) # noqa

    def search_time(self):
        """ This gets a time from the user and returns it."""
        valid_variable = True
        self.clear()
        while True:
            if valid_variable is False:
                self.clear()
                print("  That is not a valid number for minutes.\n" +
                      "  Please enter a number like '15'.  \n")
            try:
                minutes = int(input("  Please enter the minutes " +
                                    "spent on the task.  "))
            except ValueError:
                valid_variable = False
            else:
                break
        return minutes

    def show_template(self, entry_num, max_entries, entry, menu_options=None):
        """ This is template that is created for and used in show(). """
        self.clear()
        entry_date = datetime.datetime.strftime(entry.entry_date, '%m/%d/%Y')
        template = """
      Entry number_{} of {} by {} {}.
  Date: {}
  Title: {}
  Minutes: {}

  Notes: {}
  ----------------------------------------------------------------------------
  """.format(entry_num + 1, max_entries, entry.first_name, entry.last_name,
             entry_date, entry.title, entry.minutes, entry.notes)
        print(template)
        print("  Enter 'q' to exit to the main menu\n" +
              "  Enter 'search' to do another search.\n" +
              "  Enter 'e' to edit this work log.\n" +
              "  Enter 'g' to 'go' to another entry number.\n" +
              "  Enter 'd' to delete this work log.")
        if menu_options == 'left':
            print("  You can move left. Enter 'l' or 'left'")
        elif menu_options == 'right':
            print("  You can move right. Enter 'r' or 'right'")
        elif menu_options == 'both':
            print("  You can move left or right.\n" +
                  "  Enter 'r', 'right', 'l', or 'left'")
        menu_selector = input("  ").lower()
        return menu_selector

    def show(self, index_counter=0):
        """ Using the information in self.found_results this shows the
        user the results of a previous search. It also allows the user
        to to continue searching, edit, delete, or exit out of the
        show menu."""
        length = len(self.found_results)
        run_loop = True

        # This is incase the user deletes the only entry in the search
        # results.
        if index_counter == -1:
            if length > 0:
                index_counter = 0
            else:
                run_loop = False

        # This prevents the loop from running if not results are returned.
        elif length == 0:
            run_loop = False
            timer_counter = range(4, 0, -1)
            for second in timer_counter:
                self.clear()
                print("""
    There were no results found for your search.
  Taking you back to the search menu. In {} seconds.""".format(second))
                time.sleep(1)
            run_loop = False
            self.search()

        while run_loop:
            # This creates the menu_options variable for the show_template
            # left means the user can move left.
            # Right, both and none mean the same as there name.
            menu_options = None
            if index_counter == 0:
                if index_counter < length - 1:
                    menu_options = 'right'
            if index_counter == length - 1:
                if index_counter != 0:
                    menu_options = 'left'
            if index_counter > 0 and index_counter < length - 1:
                menu_options = 'both'

            menu_selector = self.show_template(index_counter, length,
                                               self.found_results
                                               [index_counter],
                                               menu_options)

            # This controls if the user can actually go left and right.
            # If not, then the user is told and can choice what to do next.
            if menu_selector == 'r' or menu_selector == 'right':
                if index_counter >= length - 1:
                    timer_counter = range(3, 0, -1)
                    for seconds in timer_counter:
                        self.clear()
                        print("\n    You can not go right.\n" +
                              "  Returning to your search in {} seconds."
                              .format(seconds))
                        time.sleep(1)
                else:
                    index_counter += 1
            elif menu_selector == 'g' or menu_selector == 'go':
                clear_screen = False
                while True:
                    if clear_screen:
                        self.clear()
                        print('\n  You must enter an integer between 1 and {}'
                              .format(length))
                    try:
                        entry_num = int(input('\n  Which entry do you want ' +
                                              'to go to?' +
                                              '\n  You can move to any entry' +
                                              ' between' +
                                              ' 1 and {}.'.format(length)))
                    except ValueError:
                        clear_screen = True
                    else:
                        if entry_num >= 1 and entry_num <= length:
                            break
                        else:
                            clear_screen = True
                index_counter = entry_num - 1
            elif menu_selector == 'l' or menu_selector == 'left':
                if index_counter <= 0:
                    timer_counter = range(3, 0, -1)
                    for seconds in timer_counter:
                        self.clear()
                        print("\n    You can not go left.\n" +
                              "  Returning to your search in {} seconds."
                              .format(seconds))
                        time.sleep(1)
                else:
                    index_counter -= 1
            elif menu_selector == 'q' or menu_selector == 'quit':
                break
            elif menu_selector == 's' or menu_selector == 'search':
                run_loop = False
                self.search()
            elif menu_selector == 'e' or menu_selector == 'edit':
                user_date, title, minutes, notes, stop = \
                    self.editor(self.found_results[index_counter])
                if stop:
                    break
                # This sends all of the information to DatabaseIntermediary for
                # further processing
                self.db.editor(self.found_results[index_counter],
                               n_first=self.found_results[index_counter]
                               .first_name,
                               n_last=self.found_results[index_counter]
                               .last_name,
                               n_entry_date=user_date, n_title=title,
                               n_minutes=minutes, n_notes=notes, edit=True)
                user_date = datetime.datetime.strptime(user_date, '%m/%d/%Y')
                self.found_results[index_counter].entry_date = user_date
                self.found_results[index_counter].title = title
                self.found_results[index_counter].minutes = minutes
                self.found_results[index_counter].notes = notes
                self.show(index_counter=index_counter)
                break

            elif menu_selector == 'd' or menu_selector == 'delete':
                delete = input('\n  Are you sure you want to delete this ' +
                               "entry? N/y'").lower()
                if delete == 'y':
                    self.db.editor(self.found_results[index_counter])
                    del self.found_results[index_counter]
                    index_counter -= 1
                    self.show(index_counter=index_counter)
                    break
