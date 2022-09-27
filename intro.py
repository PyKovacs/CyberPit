from users import UserHandler, new_user_sequence
from base import clear_console

def starting_sequence():
    print('\nWELCOME TO THE CYBER PIT!')
    user, new = UserHandler().load_user()
    clear_console()
    print('\n--------------------------')
    print(f'Welcome {user.name}!')
    if new:
        new_user_sequence(user)
    print(f'Your current balance is {user.balance} bitcoins.')
    