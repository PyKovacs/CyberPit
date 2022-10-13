from time import sleep
from typing import Dict

from src.pit import ThePit
from src.users import User, UserManager
from src.utils import clear_console


class MainMenu:

    def __init__(self, user: User, pit: ThePit) -> None:
        self.user = user
        self.pit = pit


    def get_menu_options(self) -> Dict[str, str]:
        '''
        Returns main menu options list
        '''
        return {'battle': 'Enter the PIT and fight!', 
                'robot': 'Shows your robot details.', 
                'shop': 'Enter the robot shop.', 
                'quit': 'Exit the game.'}

    def get_menu(self) -> str:
        '''
        Returns str of main menu options
        '''
        menu = f'\n{"":#^20}'
        menu += f'\n-{"MAIN MENU":^18}-\n'
        for item, desc in self.get_menu_options().items():
            menu += f'\no {item.capitalize()} - {desc}'
        menu += f'\n{"":#^20}'
        return menu

    def present_menu(self) -> None:
        '''
        Presents the main menu
        '''
        details = False
        while True:
            clear_console()
            print('----------------------------')
            print(self.user.name.upper())
            if self.user.robot:
                if details:
                    print(self.user.robot)
                else:
                    print(f'Your current robot: {self.user.robot.name}')
            else:
                print('You don\'t have any robot yet.')
            print('Your balance: ' + self.user.get_balance(full=False))
            print(self.get_menu())
            details = False
            if self.execute_option() == 'robot':
                details = True
    
    def execute_option(self) -> str:
        print('\nPick your action.')
        print(tuple(self.get_menu_options().keys()))
        action = input('').lower()
        if action == 'quit':
            exit(0)
        if action == 'shop':
            clear_console()
            self.user.buy_robot()
        if action == 'battle':
            clear_console()
            self.pit.intro()
        return action
            

