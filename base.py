
import os


def clear_console():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')







''' 
    @dataclass
    class Rich(RobotBase):
        health: int = 15
        energy: int = 15
        money: int = 30
        desc: str = 'Efficient build, more money for weapons.'

    @dataclass
    class Brute(RobotBase):
        health: int = 45
        money: int = 15
        dodge_chance: int = 5
        miss_chance: int = 15
        desc: str = 'Super strong materials, very high HP.'

    @dataclass
    class Duracell(RobotBase):
        health: int = 15
        energy: int = 35
        money: int = 30
        miss_chance : int = 10
        desc: str = 'Improved power supply, increased energy.'
'''