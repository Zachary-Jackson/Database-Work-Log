import time
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
        main()
    else:
        print("\nUntil next time, bon voyage!")


def name_picker():
    """ This gathers a single users first and last name, or returns
    all names. """
    while True:
        clear()
        clear_screen = True
        while True:
            if clear_screen:
                clear()
            else:
                for _ in range(3, 0, -1):
                    clear()
                    print("\n  Please enter a first name only.")
                    print("  You can enter another name in {} seconds".format(
                                                                      _))
                    time.sleep(1)
                    clear()
            first_name = input("\n  Please enter a first name.  \n  ").title()\
                                                                      .strip()
            if ' ' in first_name or first_name == '':
                clear_screen = False
            else:
                break

        clear_screen = False
        while True:
            if clear_screen:
                for _ in range(3, 0, -1):
                    clear()
                    print("\n  Please enter a last name with no " +
                          "middle names.\n")
                    print("  You can enter another name in {} seconds".format(
                                                                      _))
                    time.sleep(1)
                    clear()
            last_name = input("\n  Please enter a last name.  \n  ").title()\
                                                                    .strip()
            if ' ' in last_name or last_name == '':
                clear_screen = True
            else:
                break

        good_name = input("\n  Is {} {} the name you want to use? Y/n  "
                          .format(first_name, last_name)).lower()
        if good_name != 'n':
            return first_name, last_name


def main():
    """ This is the primary menu for work_log.py and gathers information
    to call on the correct class. The user is also allowed to quit and
    end the script."""

    first_name, last_name = name_picker()
    # temp all names
    all_names = False
    main_loop = True
    while main_loop:
        # This clears the screen on every new instance of the loop
        clear()
        menu_item = EntryChanger()
        # This is the primary menu prompting the user what they want to do.
        print('                                 Main Menu\n'
              '-----------------------------------------' +
              '---------------------------------------\n')
        print('    Please enter the option you would like to select')
        if all_names:
            print('.\n\n')
        else:
            print('    {} {}.\n\n'.format(first_name, last_name))

        menu_selector = input('  a) Add an entery to the program.\n' +
                              '  b) Search exsisting entries.\n' +
                              '  c) Show all work log entries.\n' +
                              '  d) Enter a new name.\n'
                              '  e) Exit the program.  '.lower())
        if menu_selector == 'a)' or menu_selector == 'a' \
                or menu_selector == 'add':
            menu_item.run_entry_changer(first_name, last_name, 'add')
        if menu_selector == 'b)' or menu_selector == 'b' \
                or menu_selector == 'search':
            menu_item.run_entry_changer('search')
        if menu_selector == 'c' or menu_selector == 'c)' \
                or menu_selector == 'change':
            menu_item.show_all()

        if menu_selector == 'd' or menu_selector == 'd)' \
                or menu_selector == 'all':
            first_name, last_name = name_picker()

        if menu_selector == 'e' or menu_selector == 'e)' \
                or menu_selector == 'q' or menu_selector == 'quit':
            print("\nThank you for using the work log application!")
            main_loop = False


if __name__ == '__main__':
    # This makes sure that the script does not run if imported
    welcome()
