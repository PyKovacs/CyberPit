from time import sleep
import random
import string
from typing import Optional

from src.robots import Robot, RobotManager
from src.users import UserManager
from src.utils import clear_console, delayed_typing

class ThePit:
    def __init__(self, robot_manager: RobotManager, user_manager: UserManager):
        self.robot_manager = robot_manager
        self.user_manager = user_manager
        self.player = user_manager.current_user
        self.player_robot = self.player.robot

    def intro(self):
        print('Ready for the fight?\n')
        sleep(2)
        self.opponent_robot = self.assign_opponent()
        self.opp_name = self._random_name()
        print(f'Today, you stand against {self.opp_name}.')
        print(self.opponent_robot)
        sleep(1)
        print('Last chance to give up.',
                'Type "coward" to go back to main menu.',
                'Any other key hit will throw you to the pit.',
                sep='\n')
        if input('') == 'coward':
            return
        self.fight()
            

    def assign_opponent(self) -> Robot:
        opp_build = random.choice(self.robot_manager.get_all_build_names())
        return Robot(self.robot_manager.get_build_data(opp_build))

    def fight(self):
        clear_console()
        self.pit_talk()
        while True:
            if self.player_robot.health <= 0 or self.opponent_robot.health <= 0:
                # match finished
                break
            self.round()
        win = self._evaluate_win()
        if win is None:
            delayed_typing('Unbelievable! Its a draw!')
            return
        delayed_typing('Aaaand the winner iiiiiiis.....')
        if win:
            delayed_typing(self.player.name.capitalize())
            sleep(2)
            return
        delayed_typing(self.opp_name)
        sleep(2)

    def pit_talk(self):
        delayed_typing('LAAAAADIEEEES AND GENTLEMEEEEEN...')
        sleep(0.5)
        delayed_typing('Welcome, to THE CYBER PIT!\n')
        sleep(0.2)
        delayed_typing('A place where metal meets metal in the MOST BRUUUUTAL ROOBOOOT FIIIGTHS!')
        sleep(0.5)
        delayed_typing('Hang tight, as TONIIIGHT you will experience the clash of titans.')
        delayed_typing(f'Tonight, {self.player.name.capitalize()} will confront {self.opp_name} in unprecedented cyber dance.\n')
        sleep(2)
        delayed_typing(f'LET THE SHOOOOOOOW BEGIIIIIIIINNN !!!!', 0.08)
        sleep(2)
    
    def round(self):
        self.player_turn()
        self.opponent_turn()

    def player_turn(self):
        print(f'Your weapons: {self.player.robot.weapons}')
        print('You have following options:\n',
              ' - type the weapon name to use it',
              ' - type "stats" for your robot current stats',
              ' - type "enemy" for your enemy\'s stats',
              sep='\n')
        while True:
            action = input('What will it be? ').lower()
            if action == 'stats':
                print(self.player_robot)
            if action == 'enemy':
                print(self.opponent_robot)
            if action in self.player.robot.weapons:
                self.attack(action, self.player_robot, self.opponent_robot)
                break

    def opponent_turn(self):
            weapon = random.choice(self.opponent_robot.weapons)
            self.attack(weapon, self.opponent_robot, self.player_robot)

    def attack(self, weapon: str, attacking: Robot, attacked: Robot):
        delayed_typing(f'Loading {weapon} ...')
        sleep(1)
        damage_points = attacking.use_weapon(weapon)
        if not damage_points:
            print(f'{attacking.name} missed !!!')   # TODO Think about putting name here - maybe create a USer for opponent, or create name for robot (better)
            return
        hit = attacked.take_damage(damage_points)
        if not hit:
            print(f'{attacked.name} dodged !!!')
            return
        print(f'{attacked.name} took {damage_points} points of damage !!!')
        return

    def _evaluate_win(self) -> Optional[bool]:
        '''
        Returns the winner of the match
        '''
        if self.opponent_robot.health > self.player_robot.health:
            return False
        elif self.opponent_robot.health < self.player_robot.health:
            return True
        else:
            return None


    def _random_name(self):
        first = random.choice(string.ascii_letters)
        second = random.choice(string.ascii_letters)
        num = random.randint(100,999)
        return f'{first}{second}-{num}'
