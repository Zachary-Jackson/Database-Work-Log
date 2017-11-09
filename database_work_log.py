import os

from entry_changer import EntryChanger


def clear():
    """ This function clears the screen for easier reading and use."""
    os.system('cls' if os.name == 'nt' else 'clear')


def welcome():
    """ This funciton welcomes the user to the program. """
    clear()
    menu_selector = input("""
    Welcome to the work log application!

  Here you may add or delete tasks for your work log.
  Enter anything to continue or enter 'q' to quit. """).lower()
    if menu_selector != 'q':
        return True
    else:
        print("\nUntil next time, bon voyage!")
        return False


def main_initalization():
    """ This creates a few values for main."""
    menu_item = EntryChanger()
    first_name, last_name = menu_item.run_entry_changer(command='get names')
    return menu_item, first_name, last_name


def main_all_names():
    """ Returns to main() if the user wants to use all names or not."""
    all_names = input("\n  Do you want to search via all names " +
                      "or your name?\n" +
                      "  Enter 'my' to search by your name, " +
                      'otherwise, all will be searched.  ').lower()
    if all_names != 'my':
        return True
    else:
        return False


def main(menu_item, first_name, last_name):
    """ This is the primary menu for work_log.py and gathers information
    to call on the correct class. The user is also allowed to quit and
    end the script."""

    main_loop = True
    while main_loop:
        # This clears the screen on every new instance of the loop
        clear()
        # This is the primary menu prompting the user what they want to do.
        print('                                 Main Menu\n'
              '-----------------------------------------' +
              '---------------------------------------\n')
        print('    Please enter the option you would like to select')
        print('    {} {}.\n\n'.format(first_name, last_name))

        menu_selector = input('  a) Add an entery to the program.\n' +
                              '  b) Search exsisting entries.\n' +
                              '  c) Show all work log entries.\n' +
                              '  d) Enter a new name.\n'
                              '  e) Exit the program.  '.lower())
        if menu_selector == 'a)' or menu_selector == 'a' \
                or menu_selector == 'add':
            first_name, last_name = menu_item.run_entry_changer(first_name,
                                                                last_name,
                                                                'add')
        if menu_selector == 'b)' or menu_selector == 'b' \
                or menu_selector == 'search':
            all_names = main_all_names()
            first_name, last_name = menu_item.run_entry_changer(first_name,
                                                                last_name,
                                                                'search',
                                                                all_names= # noqa
                                                                all_names)
        if menu_selector == 'c' or menu_selector == 'c)' \
                or menu_selector == 'change':
            all_names = main_all_names()
            first_name, last_name = menu_item.run_entry_changer(first_name,
                                                                last_name,
                                                                'show all',
                                                                all_names= # noqa
                                                                all_names)
        if menu_selector == 'd' or menu_selector == 'd)' \
                or menu_selector == 'all':
            first_name, last_name = menu_item.name_picker()

        if menu_selector == 'e' or menu_selector == 'e)' \
                or menu_selector == 'q' or menu_selector == 'quit':
            print("\nThank you for using the work log application!")
            main_loop = False
    return True


if __name__ == '__main__':
    # This makes sure that the script does not run if imported
    if welcome():
        menu_item, first_name, last_name = main_initalization()
        main(menu_item, first_name, last_name)
