from src.users import UserManager, PwdManager
from src.robots import RobotManager
from src.db import DBHandler
from src.menu import MainMenu
from src.utils import theme

class Game:
    def __init__(self, user_manager: UserManager, main_menu: MainMenu) -> None:
        self.user_manager = user_manager
        self.main_menu = main_menu
        self.user = self.user_manager.read_username()
        theme()
    
    def run(self):
        '''
        Game flow sequence.
        '''
        self.main_menu.present_menu(self.user)

def main():
    try:
        game = Game(
            UserManager(
                DBHandler(), 
                PwdManager(), 
                RobotManager()), 
            MainMenu())
        game.run()
    except KeyboardInterrupt:
        print('\nYou pressed a magic combination of keys (ctrl + c), quitting the game...')

if __name__ == '__main__':
    main()
