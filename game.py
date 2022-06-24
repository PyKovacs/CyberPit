from dataclasses import dataclass
from typing import List

import base

print('\nWELCOME TO THE CYBER PIT!')
print('Robot protocols available:\n')
print(base.RobotProtocols.showcase())

protocolname = None
while protocolname not in base.RobotProtocols.all_protocol_names:
    protocolname = input('Choose your robot protocol:\n'+f'{base.RobotProtocols.all_protocol_names}\n').upper() # TODO dorobit legendu
protocolclass = base.RobotProtocols.get_protocolclass_from_protocolname(protocolname.upper())

name = str(input('Good choice! Now name your machine:\n'))
while not name:
    protocol = input('Name your robot:\n')

player_robot = protocolclass(name)
print('This is your robot:\n', player_robot)

print('{} the {} needs some weapons to fight.'.format(name, protocolname))