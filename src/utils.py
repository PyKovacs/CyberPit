import os
from time import sleep
from typing import Tuple

THEME_TITLE: Tuple = (
'##########################################################',
'##########################  ##############################',
'#####      ###############  ##############################',
'####  ####  ##############  #########     ####   ###   ###',
'###  ##########  ####   ##      ####  ###  ###      ######',
'###  ###########  ##   ###  ###  ###       ###   #########',
'####  ####  ######   #####  ###  ###  ########   #########',
'#####     #######   ######      #####     ####   #########',
'################   #######################################',
'###############   ########################################',
'#             #######                                    #',
'#           ####   ###                                   #',
'#          ####   ###        ##         ####             #',
'#         ########                   #########           #',
'#        ####             ####        ####               #',
'#       ####             ####        ####  ##            #',
'#      ####             ####        ########             #',
'##########################################################',
'                                               by PyKovacs'
)

def clear_console() -> None:
    '''
    Clears the console
    '''
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')

def delayed_typing(text: str, sleep_interval: float = 0.05) -> None:
    '''
    Print the text with sleep between characters.
    '''
    for char in text:
        print(char, end="", flush=True)
        sleep(sleep_interval)
    print()

def theme() -> None:
    '''
    Theme show at the beginning of the game.
    '''
    clear_console()
    sleep_time = 0.008
    for line in THEME_TITLE:
        for char in line:
            if char == 'b':
                sleep(0.5)
                sleep_time = 0.1
            print(char, end="", flush=True)
            sleep(sleep_time)
        sleep_time /= 1.15
        print()
    sleep(3)
    clear_console()
        
