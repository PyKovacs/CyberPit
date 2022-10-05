from users import UserHandler, User, new_user_sequence
from utils import clear_console
from time import sleep


def starting_sequence(user_handler: UserHandler) -> User:
    '''
    Starting sequence for user login/creation.
    Returns user object
    '''
    print('\nWELCOME TO THE CYBER PIT!')
    user, new = user_handler.user_login()
    clear_console()
    if new:
        new_user_sequence(user)
        clear_console()
    print('\n--------------------------')
    print(f'Welcome {user.name}!')
    sleep(1)
    print(f'Your current robot: \n{user.robot}')
    return user
