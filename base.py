from dataclasses import dataclass
from typing import List



@dataclass(frozen=True)
class Weapon:
    cost: int
    damage: int
    consumption: int
    protocol: str
    special: List
    desc: str

    @staticmethod
    def get_weapon():
        laser = Weapon(5, 2, 2, 'heat', [], 'Basic weapon without special effects.')
        bumper = Weapon(10, 1, 1, 'force', ['startle', 'accurate'], 'Reinforced metal plate on front. Not much damage, however 10% chance to startle the enemy. Also never misses the target.') # enemy skips round, never miss
        # self.flamethrower = self.Weapon(15, 5, 7, 'heat', ['overheat','selfko'], '')  # causes more damage to enemy but also self
        # self.hammer = self.Weapon(10, 10, 7, 'force', ['notaccurate']) # greater chance to miss
        # self.saw = self.Weapon(5, 2, 5, 'cut', ['cutcable']) # increase miss for enemy on next round
        # self.spike = self.Weapon(2, 2, 1, 'cut', ['accurate'])
        # self.flipper = self.Weapon(20, 0, 10, 'force', ['ko']) # low chance but KO if success





class RobotProtocols:

    @dataclass
    class RobotBase:
        name: str = ''
        protocol: str = ''
        health: int = 20
        energy: int = 20
        money: int = 20
        dodge_chance: int = 10
        miss_chance: int = 5
        desc: str = ''

    @dataclass
    class Heavy(RobotBase):
        protocol: str = 'HEAVY'
        health: int = 30
        dodge_chance: int = 5
        desc: str = 'Heavy tank, increased HP.'

    @dataclass
    class Light(RobotBase):
        protocol: str = 'LIGHT'
        health: int = 15
        money: int = 25
        dodge_chance: int = 20
        desc: str = 'Light construction, good at dodging.'
    
    @dataclass
    class Rich(RobotBase):
        protocol: str = 'RICH'
        health: int = 15
        energy: int = 15
        money: int = 30
        desc: str = 'Efficient build, more money for weapons.'

    @dataclass
    class Brute(RobotBase):
        protocol: str = 'BRUTE'
        health: int = 45
        money: int = 15
        dodge_chance: int = 5
        miss_chance: int = 15
        desc: str = 'Super strong materials, very high HP.'

    @dataclass
    class Duracell(RobotBase):
        protocol: str = 'DURACELL'
        health: int = 15
        energy: int = 35
        money: int = 30
        miss_chance : int = 10
        desc: str = 'Improved power supply, increased energy.'

    all_protocols= [subcls for subcls in RobotBase.__subclasses__()]
    all_protocol_names= [protocol.protocol for protocol in all_protocols]

    @classmethod
    def showcase(cls):
        showcase = ''
        for r_protocol in cls.all_protocols:
            showcase += ('*** {} ***\n{}\n\nHealth: \t{}\nEnergy: \t{}\nMoney: \t\t{}\nDodge chance:  \t{}%\nMiss chance:  \t{}%\n\n'
                        .format(r_protocol.protocol, r_protocol.desc, r_protocol.health, r_protocol.energy, r_protocol.money, r_protocol.dodge_chance, r_protocol.miss_chance))
        return showcase
    
    @classmethod
    def get_protocolclass_from_protocolname(cls, protocolname):
        return [protocolclass for protocolclass in cls.all_protocols if protocolclass.protocol == protocolname][0]
