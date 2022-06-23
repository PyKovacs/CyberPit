from dataclasses import dataclass
from typing import List

import base

print('\nWELCOME TO THE CYBER PIT!')
print('Robot types available:\n')
print(base.RobotTypes.showcase())

type = None
while type not in base.RobotTypes.all_type_names:
    type = input('Choose your robot type:\n'+f'{base.RobotTypes.all_type_names}\n').upper() # TODO dorobit legendu

name = str(input('Good choice! Now name your machine:\n'))
while not name:
    type = input('Name your robot:\n')

print('{} the {} needs some weapons to fight.'.format(name, type))