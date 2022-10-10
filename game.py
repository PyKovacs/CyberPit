from src.users import UserManager, PwdManager
from src.robots import RobotManager
from src.db import DBHandler
from src.menu import MainMenu
from src.pit import ThePit
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
        self.pit = ThePit(self.robot_manager, self.user_manager)
        self.main_menu = MainMenu(self.user, self.pit)
        theme()
    
    def run(self):
        '''
        Game flow sequence.
        '''
        self.main_menu.present_menu()

def main():
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print('\nYou pressed a magic combination of keys (ctrl + c), quitting the game...')

if __name__ == '__main__':
    main()
