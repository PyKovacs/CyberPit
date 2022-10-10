from time import sleep
import random

from src.robots import Robot, RobotBuilds

class ThePit:

    def intro(self):
        print('WELCOME! To The Pit!')
        print('Ready for the fight?\n')
        sleep(2)
        opponent = self.assign_opponent()
        print(f'Today, you stand against {opponent.name}.')
        sleep(1)
        # add an option to surrender

    def assign_opponent(self) -> Robot:
        opp_name = random.choice(RobotBuilds._get_all_names())
        return RobotBuilds._get_build_obj(opp_name)

    def fight(self):
        pass

