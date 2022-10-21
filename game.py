from src.db import DBHandler
from src.menu import MainMenu
from src.robots import RobotManager
from src.users import PwdManager, UserManager
from src.utils import theme


class Game:
    def __init__(self) -> None:
        self.db_handler = DBHandler()
        self.pwd_manager = PwdManager()
        self.robot_manager = RobotManager()
        self.user_manager = UserManager(self.db_handler,
                                self.pwd_manager,
                                self.robot_manager)
        self.user = self.user_manager.read_username()
        self.main_menu = MainMenu(self.user, self.robot_manager)
        theme()

    def run(self):
        '''
        Game flow sequence.
        '''
        self.main_menu.present_menu()

def main():
    '''
    Main function running the game.
    '''
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print('\nYou pressed a magic combination of keys (ctrl + c), quitting the game...')

if __name__ == '__main__':
    main()
