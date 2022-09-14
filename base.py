
import os
from user_mgmt import User
from dcs import RobotBase

def clear_console():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')

def new_user_sequence(user: User):
    print(f'It seems you are new here.')
    user.set_balance(500)
    print('You were granted 500 bitcoins for a start, use them wisely!')
    print(RobotsHandler.showcase())
    user.set_robot(input('For a start, pick a robot to buy:\n'))


class RobotsHandler:

    all_builds= [subcls for subcls in RobotBase.__subclasses__()]
    all_build_names= [build.__name__ for build in all_builds]

    @classmethod
    def showcase(cls):
        title = '***** {} *****'
        showcase = ''
        for r_build in cls.all_builds:
            showcase += (f'{title.format(r_build.__name__.upper())}\n -> {r_build.desc}\n')
            for key, value in r_build.__dict__.items():
                if '__' not in str(key):
                    showcase += f'{key.capitalize()}:\t\t {value}\n'
            showcase += '********************\n\n'
        return showcase
    
    @classmethod
    def get_buildclass_from_buildname(cls, buildname):
        return [buildclass for buildclass in cls.all_builds if buildclass.__name__ == buildname.capitalize()][0]


''' 
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
'''