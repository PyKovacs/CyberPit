from __future__ import annotations

import json
import random
from abc import ABC
from time import sleep
from typing import Dict, List, Tuple, Union

WEAPONS = {
    'laser': 6,
    'bumper': 3,
    'saw': 4,
    'flipper': 7,
    'plasma_gun': 12,
    'flame_thrower': 9,
    'spike': 2
}

BLANK_BUILD: Dict[str, Union[str, int, List[str]]]
BLANK_BUILD = {
        "name": "",
        "build": "",
        "desc": "",
        "weapons": [],
        "health": 0,
        "energy": 0,
        "dodge_chance": 0,
        "miss_chance": 0,
        "cost": 0
}

PATH_TO_BUILDS = 'data/builds.json'

class RobotBase(ABC):
    name: str
    build: str
    health: int
    energy: int
    dodge_chance: int
    miss_chance: int
    desc: str
    cost: int
    weapons: List[str]

class Robot(RobotBase):

    def __init__(self, name, init_data: Dict[str, Union[str, int, List[str]]]) -> None:
        self.name = name
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

    def take_damage(self, damage: int) -> bool:
        '''
        Reduce the HP by damage.
        Return False if dodged, else True
        '''
        dodged_int = random.randint(1,100)
        if dodged_int < self.dodge_chance:
            return False
        self.health -= damage
        return True

    def get_weapon_energy(self, weapon) -> int:
        '''
        Return energy and damage points of provided weapon.
        '''
        return WEAPONS.get(weapon, 0)

    def use_weapon(self, weapon: str) -> int:
        '''
        Reduce the energy and calculate miss.
        Return -1 if not enough energy, 0 if missed, else damage value.
        '''
        energy_cost = WEAPONS[weapon]
        if self.energy < energy_cost:
            return -1
        self.energy -= energy_cost
        miss_int = random.randint(1,100)
        if miss_int < self.miss_chance:
            return 0
        return energy_cost

    def is_exhausted(self) -> bool:
        '''
        Returns False if robot has no energy left for using any weapon
        '''
        energy_needed=min([energy for weapon, energy in WEAPONS.items() if weapon in self.weapons])
        if self.energy >= energy_needed:
            return False
        return True

    def reset(self, robot_manager: RobotManager) -> None:
        '''
        Resets the energy and health.
        '''
        build_data = robot_manager.get_build_data(self.build)
        assert isinstance(build_data['health'], int)
        assert isinstance(build_data['energy'], int)
        self.health, self.energy = build_data['health'], build_data['energy']


class RobotManager:
    '''
    Managing the actions around robots.
    '''

    def __init__(self) -> None:
        with open(PATH_TO_BUILDS, 'r') as builds_file:
            self.builds: Dict[str, Dict[str, Union[str, int, List[str]]]]
            self.builds = json.load(builds_file)
        self.blank_build = Robot("", BLANK_BUILD)
    
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
            build = Robot(build_data['build'], build_data)
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
        name = input('Name your new robot: ')
        return Robot(name, self.get_build_data(build_name))
