from src.users import UserManager, PwdManager
from src.db import DBHandler
from src.menu import MainMenu

if __name__ == '__main__':
    try:
        main_menu = MainMenu()
        user = main_menu.starting_sequence(UserManager(DBHandler(), PwdManager()))
        main_menu.present_menu(user)
    except KeyboardInterrupt:
        print('\nYou pressed a magic combination of keys (ctrl + c), quitting the game...')
