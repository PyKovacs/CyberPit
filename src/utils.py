import os
from typing import Tuple
from time import sleep

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

def theme() -> None:
    '''
    Theme show at the beginning of the game.
    '''
    clear_console()
    sleep_time = 0.008
    for line in THEME_TITLE:
        if 'PyKovacs' in line:
            sleep_time = 0.015
        for char in line:
            print(char, end="", flush=True)
            sleep(sleep_time)
        sleep_time /= 1.15
        print()
    sleep(3)
    clear_console()
        
