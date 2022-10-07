from src.users import UserManager, PwdManager, User
from src.db import DBHandler
from src.menu import MainMenu
from src.utils import clear_console, theme

class Game:
    def __init__(self, user_manager: UserManager, main_menu: MainMenu) -> None:
        self.user_manager = user_manager
        self.main_menu = main_menu

    def user_init(self, user: User):
        self.user = user

    def starting_sequence(self):
        '''
        Starting sequence for user login/creation.
        Returns user object
        '''
        self.user_init(self.user_manager.read_username())
        clear_console()
        theme()
    
    def run(self):
        self.starting_sequence()
        self.main_menu.present_menu(self.user)

def main():
    try:
        game = Game(UserManager(DBHandler(), PwdManager()), MainMenu())
        game.run()
    except KeyboardInterrupt:
        print('\nYou pressed a magic combination of keys (ctrl + c), quitting the game...')

if __name__ == '__main__':
    main()
