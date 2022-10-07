from typing import Dict
from time import sleep

from src.users import User
from src.utils import clear_console

class MainMenu:

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

    def present_menu(self, user: User) -> None:
        '''
        Presents the main menu
        '''
        details = False
        while True:
            clear_console()
            print('----------------------------')
            print(user.name.upper())
            if user.robot:
                if details:
                    print(user.robot)
                else:
                    print(f'Your current robot: {user.robot.name}')
            else:
                print('You don\'t have any robot yet.')
            print('Your balance: ' + user.get_balance(full=False))
            print(self.get_menu())
            details = False
            if self.execute_option(user) == 'robot':
                details = True
    
    def execute_option(self, user: User) -> str:
        print('\nPick your action.')
        print(tuple(self.get_menu_options().keys()))
        action = input('').lower()
        if action == 'quit':
            exit(0)
        if action == 'shop':
            clear_console()
            user.purchase_robot()
        if action == 'battle':
            print('Sorry, still in construction...')
            sleep(2)
        return action
            

