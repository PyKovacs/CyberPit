from __future__ import annotations
from abc import ABC
from typing import List, Tuple, Union, Dict
from time import sleep

import json

WEAPONS = {
    'laser': 6,
    'bumper': 3,
    'saw': 4,
    'flipper': 7,
    'plasma_gun': 12,
    'flame_thrower': 9,
    'spike': 2
}

PATH_TO_BUILDS = 'data/builds.json'

class RobotBase(ABC):
    name: str
    health: int
    energy: int
    dodge_chance: int
    miss_chance: int
    desc: str
    cost: int
    weapons: List[str]

class Robot(RobotBase):

    def __init__(self, init_data: Dict[str, Union[str, int, List[str]]]) -> None:
        for attr, value in init_data.items():
            setattr(self, attr, value)

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


class RobotManager:
    '''
    Managing the actions around robots.
    '''

    def __init__(self) -> None:
        with open(PATH_TO_BUILDS, 'r') as builds_file:
            self.builds: Dict[str, Dict[str, Union[str, int, List[str]]]]
            self.builds = json.load(builds_file)
    
    def get_all_build_names(self) -> Tuple[str,...]:
        '''
        Returns Dict of all robot builds with attributes.
        '''
        return tuple(self.builds.keys())

    def get_build_data(self, build_name: str) -> Dict[str, Union[str, int, List[str]]]:
        '''
        Returns Dict of robot build attributes.
        '''
        try:
            return self.builds[build_name]
        except KeyError:
            print(f'Failed to get build attributes.', 
            'Build name {build_name} not found!',
            sep='\n')
            exit(1)

    def showcase(self) -> str:
        '''
        Returns list of all builds with all attributes listed.
        '''
        showcase = ''
        for build_data in self.builds.values():
            build = Robot(build_data)
            showcase += str(build) + '\n'
        return showcase

    def robot_shop(self, balance: str) -> Union[str, Robot]:
        '''
        Prints welcome msg, available robot builds and prompts
        for selection. 
        Returns "cancel", empty string or Robot obj.
        '''
        print('*** WELCOME TO TO ROBOT SHOP ***',
              'Please, have a look on the finest selection.',
              balance, self.showcase(), sep='\n')
        builds = self.get_all_build_names()
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
        return Robot(self.get_build_data(build_name))
