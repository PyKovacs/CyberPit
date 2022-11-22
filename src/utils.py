import os
from dataclasses import dataclass
from time import sleep
from typing import Any, List, Tuple

THEME_TITLE: Tuple = (
'##########################################################\n',
'##########################  ##############################\n',
'#####      ###############  ##############################\n',
'####  ####  ##############  #########     ####   ###   ###\n',
'###  ##########  ####   ##      ####  ###  ###      ######\n',
'###  ###########  ##   ###  ###  ###       ###   #########\n',
'####  ####  ######   #####  ###  ###  ########   #########\n',
'#####     #######   ######      #####     ####   #########\n',
'################   #######################################\n',
'###############   ########################################\n',
'#             #######                                    #\n',
'#           ####   ###                                   #\n',
'#          ####   ###        ##         ####             #\n',
'#         ########                   #########           #\n',
'#        ####             ####        ####               #\n',
'#       ####             ####        ####  ##            #\n',
'#      ####             ####        ########             #\n',
'##########################################################\n',
'                                               by PyKovacs'
)

def clear_console() -> None:
    """Clear the console."""
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')

def drama_print(text: str, delay: float = 0.05) -> None:
    """Print the text with sleep between characters."""
    for char in text:
        print(char, end="", flush=True)
        sleep(delay)
    print()
  
def theme() -> None:
    """Theme show at the beginning of the game."""
    clear_console()
    try:
        sleep_time = 0.008
        for line in THEME_TITLE:
            for char in line:
                if char == 'b':
                    sleep(0.5)
                    sleep_time = 0.1
                print(char, end="", flush=True)
                sleep(sleep_time)
            sleep_time /= 1.15
        sleep(3)
    except KeyboardInterrupt:
        pass
    clear_console()

def safe_get(lst: List, idx: int, default: Any = '') -> Any:
    """
    Similar to dict .get func, return item from list,
    or default value if index error is raised.
    """
    try:
        return lst[idx]
    except IndexError:
        return default


@dataclass
class FightRecorder:
    records: str = ''

    def record_event(self, text: str, delay: float = 0.05) -> None:
        """Print the text with delayed typing and record the text."""
        self.records += text + '\n'
        drama_print(text, delay)

    def get_records(self) -> str:
        """Display all the records from recorder."""
        return self.records
