from dataclasses import dataclass, field
from typing import List
import os

def clear_console():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')


class RobotBuilds:

    @dataclass
    class RobotBase:
        health: int = 20
        energy: int = 20
        money: int = 20
        dodge_chance: int = 10
        miss_chance: int = 5

    @dataclass
    class Heavy(RobotBase):
        health: int = 30
        dodge_chance: int = 5
        desc: str = 'Heavy tank, increased HP.'

    @dataclass
    class Light(RobotBase):
        health: int = 15
        money: int = 25
        dodge_chance: int = 20
        desc: str = 'Light construction, good at dodging.'

    all_builds= [subcls for subcls in RobotBase.__subclasses__()]
    all_build_names= [build.__name__ for build in all_builds]

    @classmethod
    def showcase(cls, scope = None):
        title = '{}'
        if not scope:
            scope = cls.all_builds
            title = '*** {} ***'
        showcase = ''
        for r_build in scope:
            showcase += ('{}\n -> {}\n\nHealth: \t{}\nEnergy: \t{}\nMoney: \t\t{}\nDodge chance:  \t{}%\nMiss chance:  \t{}%\n\n'
                        .format(title.format(r_build.__name__), r_build.desc, r_build.health, r_build.energy, r_build.money, r_build.dodge_chance, r_build.miss_chance))
        return showcase
    
    @classmethod
    def get_buildclass_from_buildname(cls, buildname):
        return [buildclass for buildclass in cls.all_builds if buildclass.__name__ == buildname.capitalize()][0]


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