from typing import Dict
from time import sleep

from src.users import UserManager, User
from src.utils import clear_console, theme

class MainMenu:
    def display_menu(self) -> str:
        '''
        Returns str of main menu options
        '''
        menu = f'\n{"":#^20}'
        menu += f'\n-{"MAIN MENU":^18}-\n'
        for item, desc in self.get_menu_options().items():
            menu += f'\no {item.capitalize()} - {desc}'
        menu += f'\n{"":#^20}'
        return menu

    def run(self, user: User) -> None:
        '''
        Executes main menu
        '''
        details = False
        while True:
            clear_console()
            print(user.name.upper())
            print('----------------------------')
            if user.robot:
                if details:
                    print(user.robot)
                else:
                    print(f'Your current robot: {user.robot.name}')
            else:
                print('You don\'t have any robot yet.')
            details = False
            print('Your balance: ' + user.get_balance(full=False))
            print(self.display_menu())
            action = input(f'\nPick your action: \n{self.get_menu_options().keys()}\n')
            if action.lower() == 'shop':
                clear_console()
                user.purchase_robot()
                continue
            if action.lower() == 'robot':
                details = True
                user.robot
                continue
            if action.lower() == 'battle':
                print('Sorry, still in construction...')
                sleep(2)
                continue
            if action.lower() == 'quit':
                exit(0)
    
    def get_menu_options(self) -> Dict[str, str]:
        '''
        Returns main menu options list
        '''
        return {'battle': 'Enter the PIT and fight!', 
                'Robot': 'Shows your robot details.', 
                'shop': 'Enter the robot shop.', 
                'quit': 'Exit the game.'}

    def starting_sequence(self, user_manager: UserManager) -> User:
        '''
        Starting sequence for user login/creation.
        Returns user object
        '''
        print('\nWELCOME TO THE CYBER PIT!')
        user, new = user_manager.user_login()
        clear_console()
        if new:
            user_manager.new_user_sequence(user)
            clear_console()
        theme()
        return user
