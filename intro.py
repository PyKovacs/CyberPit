from user_mgmt import UserHandler
from base import new_user_sequence, clear_console

def starting_sequence():
    print('\nWELCOME TO THE CYBER PIT!')
    user, new = UserHandler().load_user()
    clear_console()
    print('\n--------------------------')
    print(f'Welcome {user.name}!')
    if new:
        new_user_sequence(user)
    print(f'Your current balance is {user.balance} bitcoins.')
    