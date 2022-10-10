from src.users import UserManager, PwdManager, User
from src.db import DBHandler
from src.menu import MainMenu
from src.pit import ThePit
from src.utils import clear_console, theme


class Game:
    def __init__(self, user_manager: UserManager, pit: ThePit) -> None:
        self.user_manager = user_manager
        self.pit = pit

    def user_init(self, user: User):
        '''
        Initialize the user.
        '''
        self.user = user

    def starting_sequence(self):
        '''
        Starting sequence for user login/creation.
        Displays the theme title intro.
        '''
        self.user_init(self.user_manager.read_username())
        clear_console()
        theme()
    
    def run(self):
        '''
        Game flow sequence.
        '''
        self.starting_sequence()
        self.main_menu = MainMenu(self.user, self.pit)
        self.main_menu.present_menu()

def main():
    try:
        game = Game(UserManager(DBHandler(), 
                                PwdManager()),
                    ThePit())
        game.run()
    except KeyboardInterrupt:
        print('\nYou pressed a magic combination of keys (ctrl + c), quitting the game...')

if __name__ == '__main__':
    main()
