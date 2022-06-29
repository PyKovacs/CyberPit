from dataclasses import dataclass, field
from typing import List
import os

def clear_console():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')


class Weapons:

    @dataclass
    class WeaponBase:
        pass

    @dataclass
    class Laser(WeaponBase):
        cost: int = 5
        damage: int = 2
        consumption: int = 2
        type: str = 'heat'
#        special: List = field(default_factory=lambda: ['striker'])
        desc: str = 'Basic weapon without special effects.'

        '''
        laser = Weapon(5, 2, 2, 'heat', [], 'Basic weapon without special effects.')
        bumper = Weapon(10, 1, 1, 'force', ['startle', 'accurate'], 'Reinforced metal plate on front. Not much damage, however 10% chance to startle the enemy. Also never misses the target.') # enemy skips round, never miss
        flamethrower = self.Weapon(15, 5, 7, 'heat', ['overheat','selfko'], '')  # causes more damage to enemy but also self
        hammer = self.Weapon(10, 10, 7, 'force', ['notaccurate']) # greater chance to miss
        saw = self.Weapon(5, 2, 5, 'cut', ['cutcable']) # increase miss for enemy on next round
        spike = self.Weapon(2, 2, 1, 'cut', ['accurate'])
        flipper = self.Weapon(20, 0, 10, 'force', ['ko']) # low chance but KO if success
        '''

    all_weapons= [subcls for subcls in WeaponBase.__subclasses__()]
    all_weapon_names= [weapon.__name__ for weapon in all_weapons]

    @classmethod
    def showcase(cls, scope = None):
        title = 'WEAPON: {}'
        if not scope:
            scope = cls.all_weapons
            title = '*** {} ***'
        showcase = ''
        for weapon in scope:
            showcase += ('{}\n{}\n\nCost: \t\t{}\nDamage: \t{}\nConsumption:  \t{}\nType:  \t\t{}\n'
                        .format(title.format(weapon.__name__), weapon.desc, weapon.cost, weapon.damage, weapon.consumption, weapon.type))
        return showcase



class RobotBuilds:

    @dataclass
    class RobotBase:
        health: int = 20
        energy: int = 20
        money: int = 20
        dodge_chance: int = 10
        miss_chance: int = 5

    @dataclass
    class Heavy(RobotBase):
        health: int = 30
        dodge_chance: int = 5
        desc: str = 'Heavy tank, increased HP.'

    @dataclass
    class Light(RobotBase):
        health: int = 15
        money: int = 25
        dodge_chance: int = 20
        desc: str = 'Light construction, good at dodging.'
    
    @dataclass
    class Rich(RobotBase):
        health: int = 15
        energy: int = 15
        money: int = 30
        desc: str = 'Efficient build, more money for weapons.'

    @dataclass
    class Brute(RobotBase):
        health: int = 45
        money: int = 15
        dodge_chance: int = 5
        miss_chance: int = 15
        desc: str = 'Super strong materials, very high HP.'

    @dataclass
    class Duracell(RobotBase):
        health: int = 15
        energy: int = 35
        money: int = 30
        miss_chance : int = 10
        desc: str = 'Improved power supply, increased energy.'

    all_builds= [subcls for subcls in RobotBase.__subclasses__()]
    all_build_names= [build.__name__ for build in all_builds]

    @classmethod
    def showcase(cls, scope = None):
        title = '{}'
        if not scope:
            scope = cls.all_builds
            title = '*** {} ***'
        showcase = ''
        for r_build in scope:
            showcase += ('{}\n -> {}\n\nHealth: \t{}\nEnergy: \t{}\nMoney: \t\t{}\nDodge chance:  \t{}%\nMiss chance:  \t{}%\n\n'
                        .format(title.format(r_build.__name__), r_build.desc, r_build.health, r_build.energy, r_build.money, r_build.dodge_chance, r_build.miss_chance))
        return showcase
    
    @classmethod
    def get_buildclass_from_buildname(cls, buildname):
        return [buildclass for buildclass in cls.all_builds if buildclass.__name__ == buildname.capitalize()][0]
