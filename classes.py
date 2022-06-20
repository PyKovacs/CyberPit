from dataclasses import dataclass
from pydoc import describe
from typing import List

class Weapons:

    @dataclass(frozen=True)
    class Weapon:
        cost: int
        damage: int
        consumption: int
        type: str
        special: List
        desc: str

    def __init__(self):
        self.laser = self.Weapon(5, 2, 2, 'heat', [], 'Basic weapon without special effects.')
        self.bumper = self.Weapon(10, 1, 1, 'force', ['startle', 'accurate'], 'Reinforced metal plate on front. Not much damage, however 10% chance to startle the enemy. Also never misses the target.') # enemy skips round, never miss
        # self.flamethrower = self.Weapon(15, 5, 7, 'heat', ['overheat','selfko'], '')  # causes more damage to enemy but also self
        # self.hammer = self.Weapon(10, 10, 7, 'force', ['notaccurate']) # greater chance to miss
        # self.saw = self.Weapon(5, 2, 5, 'cut', ['cutcable']) # increase miss for enemy on next round
        # self.spike = self.Weapon(2, 2, 1, 'cut', ['accurate'])
        # self.flipper = self.Weapon(20, 0, 10, 'force', ['ko']) # low chance but KO if success


class RobotTypes:

    @dataclass(frozen=True)
    class RobotType:
        name : str
        health : int = 20
        energy : int = 20
        money : int = 20
        dodge_chance : int = 10
        miss_chance : int = 5
        desc : str = None

        def showcase(self):
            return ('*** {} ***\n{}\n\nHealth: \t{}\nEnergy: \t{}\nMoney: \t{}\nDodge chance:  \t{}%\nMiss chance:  \t{}%\n'
                    .format(self.name.upper(), self.desc, self.health, self.energy, self.money, self.dodge_chance, self.miss_chance))

    def __init__(self):
        self.heavy = self.RobotType("Heavy", health=30, dodge_chance=5, desc='Heavy tank, less likely to dodge.')
        self.agile = self.RobotType("Agile", health=10, dodge_chance=20, desc='Light quick jumper, good at dodging, but low on HP.')
    
    def list_all(self):
        all = []
        for type_obj in self.__dict__.values():
            all.append(type_obj.showcase())
        return "\n\n".join(all)


@dataclass
class Robot:
    name : str
    hp : int
    energy : int
    weapons : List[object]
    type : object
