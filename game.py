import modules.intro as intro
from typing import List
from time import sleep

from modules.users import User, UserHandler
from modules.db import DBHandler
from modules.utils import clear_console

class MainMenu:
    @classmethod
    def display_menu(cls):
        menu = f'\n{"":_^20}'
        menu += f'\n-{"MAIN MENU":^18}-\n'
        for item in cls.get_menu_options():
            menu += f'\n-{item.capitalize():^18}-'
        menu += f'\n{"":-^20}'
        return menu

    @classmethod
    def run(cls, user: User):
        while True:
            clear_console()
            print(f'\nYour current robot: \n\n{user.robot}')
            user.show_balance()
            print(cls.display_menu())
            action = input(f'\nPick your action: \n{cls.get_menu_options()}\n')
            if action.lower() == 'shop':
                clear_console()
                user.purchase_robot()
                continue
            if action.lower() == 'battle':
                print('Sorry, still in construction...')
                sleep(2)
                continue
            if action.lower() == 'quit':
                exit(0)
    
    @classmethod
    def get_menu_options(cls) -> List[str]:
        return ['battle', 'shop', 'quit']



if __name__ == '__main__':
    try:
        user_handler = UserHandler(DBHandler())
        user = intro.starting_sequence(user_handler)
        print(MainMenu.run(user))
    except KeyboardInterrupt:
        print('\nYou pressed a magic combination of keys (ctrl + c), quitting the game...')

