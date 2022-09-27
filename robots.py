
from abc import ABC
from typing import Type, Dict
from dataclasses import dataclass

#Robots related dataclasses
class RobotBase(ABC):
    health: int
    energy: int
    dodge: int
    miss: int
    desc: str
    cost: int

@dataclass
class Heavy(RobotBase):
    health: int = 30
    energy: int = 20
    dodge: int = 5
    miss: int = 5
    desc: str = 'Heavy tank, increased HP.'
    cost: int = 300

@dataclass
class Light(RobotBase):
    health: int = 15
    energy: int = 20
    dodge: int = 20
    miss: int = 5
    desc: str = 'Light construction, good at dodging.'
    cost: int = 250


class RobotsHandler:

    all_builds= [subcls for subcls in RobotBase.__subclasses__()]

    @classmethod
    def get_builds(cls) -> Dict[str, Type[RobotBase]]:
        return {subcls.__name__: subcls for subcls in RobotBase.__subclasses__()}

    @classmethod
    def showcase(cls) -> str:
        title = '***** {} *****'
        showcase = ''
        for r_build in cls.all_builds:
            inst = r_build()
            showcase += (f'{title.format(r_build.__name__.upper())}\n -> {r_build.desc}\n')
            for key, value in inst.__dict__.items():
                if key == 'desc' or key.startswith('__'):
                    continue
                showcase += f'{key.capitalize()}:\t\t {value}'
                if key in ['dodge', 'miss']:
                    showcase += ' %'
                elif key == 'cost':
                    showcase += ' BTC'
                else:
                    showcase += ' points'
                showcase += '\n'
            showcase += '************************\n\n'
        return showcase
