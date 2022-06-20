from dataclasses import dataclass
from typing import List

from classes import Weapons, RobotTypes

weapons = Weapons()
robot_types = RobotTypes()

print('\nWELCOME TO THE CYBER PIT!')
print('Choose your robot type:')
print(robot_types.list_all())

type = input('What will it be?  ').lower()
while type not in robot_types.__dict__:
    type = input('Choose from existing types listed above.  ').lower()

print('Good choice.')

