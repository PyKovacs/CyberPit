from __future__ import annotations

import json
import random
import string
from abc import ABC
from enum import Enum
from time import sleep
from typing import Dict, List, Optional, Tuple, Union

from src.utils import clear_console

PATH_TO_BUILDS = 'data/builds.json'
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


class Weapons(Enum):
    SPIKE = 2
    BUMPER = 3
    SAW = 4
    LASER = 6
    FLIPPER = 7
    FLAME_THROWER = 9
    PLASMA_GUN = 12

    @classmethod
    def values(cls) -> List[int]:
        """Return list of values."""
        return [key.value for key in cls]

    @classmethod
    def get_energy(cls, weapon: str) -> int:
        """Return energy of provided weapon."""
        return cls[weapon.upper()].value


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
        self._init_data = init_data
        for attr, value in self._init_data.items():
            setattr(self, attr, value)

    def __str__(self) -> str:
        """
        User friendly print of robot object, list of attributes.

        Used in showcase as well as separately for specific Robot obj.
        """
        output = " " + 28*'_' + '\n'
        output += f'| {self.name.upper()}\n| {self.desc}\n'
        output += f'| Equipped: {self.weapons}\n|\n'
        for param, value in self.__dict__.items():
            if param in ['name', 'desc', 'weapons'] or param.startswith('_'):
                continue
            value = str(value)
            if param in ['dodge_chance', 'miss_chance']:
                value += ' %'
            elif param == 'cost':
                value += ' BTC'
            output += f'| {param.capitalize():<17}{value:>8} |\n'
        output += "|" + 27*'_' + "|" + '\n'
        return output
    
    def get_init_energy(self) -> int:
        """
        Return max energy.
        Helper method for typing purposes.
        """
        value = self._init_data.get('energy', '')
        assert isinstance(value, int), 'Internal error with robot init values.'
        return value

    def get_init_health(self) -> int:
        """
        Return max health.
        Helper method for typing purposes.
        """
        value = self._init_data.get('health', '')
        assert isinstance(value, int), 'Internal error with robot init values.'
        return value

    def take_damage(self, damage: int) -> bool:
        """
        Reduce the HP by damage amount.

        Return False if dodged, else True.
        """
        dodged_int = random.randint(1,100)
        if dodged_int < self.dodge_chance:
            return False
        self.health -= damage
        return True

    def use_weapon(self, weapon: str) -> int:
        """
        Reduce the energy and calculate miss.

        Return -1 if not enough energy, 0 if missed, else damage value.
        """
        energy_cost = Weapons.get_energy(weapon)
        if self.energy < energy_cost:
            return -1
        self.energy -= energy_cost
        miss_int = random.randint(1,100)
        if miss_int < self.miss_chance:
            return 0
        return energy_cost

    def is_exhausted(self) -> bool:
        """Return False if robot has no energy left for using any weapon."""
        energy_needed=min([energy for energy in Weapons.values()
                           if Weapons(energy).name.lower() in self.weapons])
        if self.energy >= energy_needed:
            return False
        return True

    def reset(self) -> None:
        """Reset the energy and health."""
        assert isinstance(self._init_data['health'], int)
        assert isinstance(self._init_data['energy'], int)
        self.health = self._init_data['health']
        self.energy = self._init_data['energy']


class RobotManager:
    """Managing the actions around robots."""

    def __init__(self) -> None:
        with open(PATH_TO_BUILDS, 'r') as builds_file:
            self.builds: Dict[str, Dict[str, Union[str, int, List[str]]]]
            self.builds = json.load(builds_file)
        self.blank_build = Robot("", BLANK_BUILD)

    def get_all_build_names(self) -> Tuple[str,...]:
        """Return Dict of all robot builds with attributes."""
        return tuple(self.builds.keys())

    def get_build_data(self, build_name: str) -> Dict[str, Union[str, int, List[str]]]:
        """Return Dict of specific robot build attributes."""
        try:
            return self.builds[build_name]
        except KeyError:
            print('Failed to get build attributes.',
            f'Build name {build_name} not found!',
            sep='\n')
            exit(1)

    def generate_robot(self) -> Robot:
        """Generate random robot from available builds."""
        robot_build = random.choice(self.get_all_build_names())
        robot_name = self.generate_robot_name()
        return Robot(robot_name, self.get_build_data(robot_build))

    @staticmethod
    def generate_robot_name() -> str:
        """Generate random name with 2 letters and 3 numbers in format XX-012."""
        first = random.choice(string.ascii_letters)
        second = random.choice(string.ascii_letters)
        num = random.randint(100, 999)
        return f'{first}{second}-{num}'

    def showcase(self) -> str:
        """Return user-friendly list of all builds with all attributes listed."""
        showcase = ''
        for build_data in self.builds.values():
            build = Robot(build_data['build'], build_data)
            showcase += str(build) + '\n'
        return showcase



class RobotShop:
    def __init__(self, robot_manager: RobotManager,  balance: int):
        self.robot_manager = robot_manager
        self.balance = balance

    def select_build(self) -> Optional[Dict[str, Union[str, int, List[str]]]]:
        """
        Print shop display, available robot builds and prompt for selection.

        Return build data, or None if purchase canceled.
        """
        while True:
            builds = self.robot_manager.get_all_build_names()
            self._print_shop_display(self.balance, builds)
            build_name = input('').capitalize()
            if build_name == 'Cancel':
                return None
            if build_name not in builds:
                print(f'"{build_name}" is not valid robot build.')
                sleep(2)
                continue
            if self._affordable_robot(build_name, self.balance):
                return self.robot_manager.get_build_data(build_name)

    def _print_shop_display(self, balance: int, builds: Tuple[str,...]) -> None:
        """Print the message when entering shop."""
        clear_console()
        print('*** WELCOME TO TO ROBOT SHOP ***',
              'Please, have a look on the finest selection.',
              f'Your balance: {balance} BTC\n',
              self.robot_manager.showcase(),
              'Select a robot you wish to buy.',
              builds,
              '(type "cancel" to return to main menu)',
              sep='\n')

    def _affordable_robot(self, build_name: str, balance: int) -> bool:
        """Return True if build cost is lower than balance."""
        build_cost = self.robot_manager.get_build_data(build_name).get('cost')
        assert isinstance(build_cost, int), 'ERROR in configuration!'
        if  build_cost > balance:
            print(f'You cannot afford "{build_name}".')
            sleep(2)
            return False
        return True
