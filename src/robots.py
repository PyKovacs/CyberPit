from typing import List, Union
from dataclasses import dataclass
from time import sleep

WEAPONS = {
    'laser': 6,
    'bumper': 3,
    'saw': 4,
    'flipper': 7,
    'plasma_gun': 12,
    'flame_thrower': 9,
    'spike': 2
}

@dataclass
class Robot:
    name: str
    health: int
    energy: int
    dodge_chance: int
    miss_chance: int
    desc: str
    cost: int
    weapons: List[str]

    def __str__(self) -> str:
        '''
        Representation of robot object, list of attributes.
        Used in showcase as well as separately for specific Robot obj.
        '''
        output = " " + 28*'_' + '\n'
        output += f'| {self.name.upper()}\n| {self.desc}\n'
        output += f'| Equipped: {self.weapons}\n|\n'
        for param, value in self.__dict__.items():
            if param in ['name', 'desc', 'weapons']:
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
        cost=300,
        weapons=['bumper', 'laser', 'flame_thrower', 'spike']
    )

    Light = Robot(
        name = 'Light',
        desc='Lower HP, good at dodging.',
        health=15,
        energy=20,
        dodge_chance=20,
        miss_chance=5,
        cost=250,
        weapons=['saw', 'flipper', 'laser']
    )

    Expensive = Robot(
        name = 'Expensive',
        desc='The one you cannot afford.',
        health=100,
        energy=100,
        dodge_chance=15,
        miss_chance=1,
        cost=5000,
        weapons=['flame_thrower', 'flipper', 'plasma_gun']
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

    @classmethod
    def _robot_shop(cls, balance: str) -> Union[str, Robot]:
        '''
        Prints welcome msg, available robot builds and prompts
        for selection. 
        Returns "cancel", empty string or Robot obj.
        '''
        print('*** WELCOME TO TO ROBOT SHOP ***',
              'Please, have a look on the finest selection.',
              balance, cls._showcase(), sep='\n')
        builds = tuple(cls._get_all_names())
        print('Select a robot you wish to buy.',
               builds, '(type "cancel" to return to main menu)', 
               sep='\n')
        build_name = input('').capitalize()
        if build_name == 'Cancel':
            return 'cancel'
        if build_name not in builds:
            print(f'"{build_name}" is not valid robot build.')
            sleep(2)
            return ""
        return cls._get_build_obj(build_name)
        