
from typing import List
from dataclasses import dataclass


@dataclass
class Robot:
    name: str
    health: int
    energy: int
    dodge: int
    miss: int
    desc: str
    cost: int

    def __repr__(self) -> str:
        output = f'--- {self.name.upper()} ---\n- {self.desc} -\n'
        for param, value in self.__dict__.items():
            if param in ['name', 'desc']:
                continue
            value = str(value)
            if param in ['dodge', 'miss']:
                    value += ' %'
            elif param == 'cost':
                    value += ' BTC'
            output += f'{param.capitalize()}:  {value}\n'
        return output



class RobotBuilds:
    '''
    Contains all builds of robots + helper methods.
    '''

    Heavy = Robot(
        name = 'Heavy',
        desc='Heavy tank, increased HP.',
        health=30,
        energy=20,
        dodge=5,
        miss=5,
        cost=300
    )

    Light = Robot(
        name = 'Light',
        desc='Light construction, good at dodging.',
        health=15,
        energy=20,
        dodge=20,
        miss=5,
        cost=250
    )

    Expensive = Robot(
        name = 'Expensive',
        desc='The one you cannot afford.',
        health=100,
        energy=100,
        dodge=15,
        miss=1,
        cost=5000
    )

    # Helper methods
    @classmethod
    def _get_all_names(cls) -> List[str]:
        return [build for build in dir(cls) if not build.startswith('_')]

    @classmethod
    def _get_build_obj(cls, build_name: str) -> Robot:
        '''
        Providing a build name str will return build object
        '''
        return cls.__dict__[build_name]

    @classmethod
    def _showcase(cls) -> str:
        showcase = ''
        for build_name in cls._get_all_names():
            build = cls.__dict__[build_name]
            showcase += str(build)
            showcase += '************************\n\n'
        return showcase