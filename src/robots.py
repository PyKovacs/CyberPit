from typing import List
from dataclasses import dataclass


@dataclass
class Robot:
    name: str
    health: int
    energy: int
    dodge_chance: int
    miss_chance: int
    desc: str
    cost: int

    def __str__(self) -> str:
        '''
        Representation of robot object, list of attributes.
        Used in showcase as well as separately for specific Robot obj.
        '''
        output = " " + 28*'_' + '\n'
        output += f'| {self.name.upper()}\n| {self.desc}\n|\n'
        for param, value in self.__dict__.items():
            if param in ['name', 'desc']:
                continue
            value = str(value)
            if param in ['dodge_chance', 'miss_chance']:
                    value += ' %'
            elif param == 'cost':
                    value += ' BTC'
            output += f'| {param.capitalize():<17}{value:>8} |\n'
        output += "|" + 27*'_' + "|" + '\n'
        return output


class RobotBuilds:      # TODO consider factory design pattern
    '''
    Contains all builds of robots + helper methods.
    '''

    Heavy = Robot(
        name = 'Heavy',
        desc='Heavy tank, increased HP.',
        health=30,
        energy=20,
        dodge_chance=5,
        miss_chance=5,
        cost=300
    )

    Light = Robot(
        name = 'Light',
        desc='Lower HP, good at dodging.',
        health=15,
        energy=20,
        dodge_chance=20,
        miss_chance=5,
        cost=250
    )

    Expensive = Robot(
        name = 'Expensive',
        desc='The one you cannot afford.',
        health=100,
        energy=100,
        dodge_chance=15,
        miss_chance=1,
        cost=5000
    )

    @classmethod
    def _showcase(cls) -> str:
        '''
        Returns list of all builds with all attributes listed.
        '''
        showcase = ''
        for build_name in cls._get_all_names():
            build = cls.__dict__[build_name]
            showcase += str(build) + '\n'
        return showcase

    # Helper methods
    @classmethod
    def _get_all_names(cls) -> List[str]:
        '''
        Returns all available build names (not objects).
        '''
        return [build for build in dir(cls) if not build.startswith('_')]

    @classmethod
    def _get_build_obj(cls, build_name: str) -> Robot:
        '''
        Providing a build name str returns build object.
        '''
        return cls.__dict__[build_name]
