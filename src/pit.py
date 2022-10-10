from time import sleep
import random
import string

from src.robots import Robot, RobotManager

class ThePit:
    def __init__(self, robot_manager: RobotManager):
        self.robot_manager = robot_manager

    def intro(self):
        print('WELCOME! To The Pit!')
        print('Ready for the fight?\n')
        sleep(2)
        opponent = self.assign_opponent()
        opp_name = self._random_name()
        print(f'Today, you stand against {opp_name}.')
        print(opponent)
        sleep(1)
        # add an option to surrender

    def assign_opponent(self) -> Robot:
        opp_build = random.choice(self.robot_manager.get_all_build_names())
        return Robot(self.robot_manager.get_build_data(opp_build))

    def fight(self):
        pass

    def _random_name(self):
        first = random.choice(string.ascii_letters)
        second = random.choice(string.ascii_letters)
        num = random.choice([x for x in range(100, 999)])
        return f'{first}{second}-{num}'
