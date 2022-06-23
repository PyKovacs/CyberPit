from dataclasses import dataclass
from typing import List



@dataclass(frozen=True)
class Weapon:
    cost: int
    damage: int
    consumption: int
    type: str
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


@dataclass
class RobotBase:
    name : str = ''
    type : str = ''
    health : int = 20
    energy : int = 20
    money : int = 20
    dodge_chance : int = 10
    miss_chance : int = 5
    desc : str = ''

    def __init__(self):
        self.heavy = self.RobotType('Heavy', health=30, dodge_chance=5, desc='Heavy tank, has a low chance to dodge attacks.')
        self.agile = self.RobotType('Agile', health=10, dodge_chance=20, desc='Light construction, good at dodging, but low on HP.')
    
    def list_all(self):
        all = []
        for type_obj in self.__dict__.values():
            all.append(type_obj.showcase())
        return "\n\n".join(all)


class RobotTypes:
    class Heavy(RobotBase):
        type: str = 'HEAVY'
        health : int = 30
        dodge_chance : int = 5
        desc : str = 'Heavy tank, increased HP.'

    class Light(RobotBase):
        type: str = 'LIGHT'
        health : int = 15
        money : int = 25
        dodge_chance : int = 20
        desc : str = 'Light construction, good at dodging.'
    
    class Rich(RobotBase):
        type: str = 'RICH'
        health : int = 15
        energy : int = 15
        money : int = 30
        desc : str = 'Efficient build, more money for weapons.'

    class Brute(RobotBase):
        type: str = 'BRUTE'
        health : int = 45
        money : int = 15
        dodge_chance : int = 5
        miss_chance : int = 15
        desc : str = 'Super strong materials, very high HP.'

    class Duracell(RobotBase):
        type: str = 'DURACELL'
        health : int = 15
        energy : int = 35
        money : int = 30
        miss_chance : int = 10
        desc : str = 'Improved power supply, increased energy.'

    all_types= [subcls for subcls in RobotBase.__subclasses__()]
    all_type_names= [type.type for type in all_types]

    @classmethod
    def showcase(cls):
        showcase = ''
        for r_type in cls.all_types:
            showcase += ('*** {} ***\n{}\n\nHealth: \t{}\nEnergy: \t{}\nMoney: \t\t{}\nDodge chance:  \t{}%\nMiss chance:  \t{}%\n\n'
                        .format(r_type.type, r_type.desc, r_type.health, r_type.energy, r_type.money, r_type.dodge_chance, r_type.miss_chance))
        return showcase

    


@dataclass
class Robot:
    name : str
    hp : int
    energy : int
    weapons : List[object]
    type : object
