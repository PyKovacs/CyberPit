import os

def clear_console() -> None:
    '''
    Clears the console
    '''
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')

