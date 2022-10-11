from time import sleep
import random
import string
from typing import Optional

from src.robots import Robot, RobotManager, WEAPONS
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
        print(f'You stand against {self.opp_name}.')
        print(self.opponent_robot)
        self.opponent_robot.name = self.opp_name
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
        return Robot(opp_build, self.robot_manager.get_build_data(opp_build))

    def fight(self):
        clear_console()
        self.pit_talk()
        self.exhausted = set()
        round_count = 1
        while True:
            if self.player_robot.health <= 0 or self.opponent_robot.health <= 0:
                # match finished
                self.announce_winner(self._evaluate_win())
                break
            if len(self.exhausted) == 2:
                self.exhausted_outcome()
                break
            self.round(round_count)
            round_count += 1
        
        

    def pit_talk(self):
        delayed_typing('LAAAAADIEEEES AND GENTLEMEEEEEN...')
        sleep(0.5)
        delayed_typing('Welcome, to THE CYBER PIT!\n')
        sleep(0.2)
        delayed_typing('A place where metal meets metal in the MOST BRUUUUTAL ROOBOOOT FIIIGTHS!')
        sleep(0.5)
        delayed_typing('Hang tight, as TONIIIGHT you will experience the clash of titans.')
        delayed_typing(f'Tonight, {self.player_robot.name} will confront {self.opponent_robot.name} in unprecedented cyber dance.\n')
        sleep(2)
        delayed_typing(f'LET THE SHOOOOOOOW BEGIIIIIIIINNN !!!!', 0.08)
        sleep(2)
    
    def round(self, round_count):
        print(f'-------- ROUND {round_count} --------')
        for playing_robot in (self.player_robot, self.opponent_robot):
            energy_needed=min([energy for weapon, energy in WEAPONS.items() if weapon in playing_robot.weapons])
            if not playing_robot.energy > energy_needed:
                delayed_typing(f' -> {playing_robot.name} is out of energy.')
                self.exhausted.add(playing_robot)
                continue
            if playing_robot == self.player_robot:
                self.player_turn()
            else:                
                self.opponent_turn()
        print(f'------------------------------------')

    def player_turn(self):
        print(f'\nYour weapons: {self.player.robot.weapons}')
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
        delayed_typing(f' -> {attacking.name} loading {weapon} ...')
        sleep(1)
        damage_points = attacking.use_weapon(weapon)
        if not damage_points:
            print(f'  -> {attacking.name} missed !!!')
            return
        hit = attacked.take_damage(damage_points)
        if not hit:
            print(f'  -> {attacked.name} dodged !!!')
            return
        print(f'  -> {attacked.name} took {damage_points} points of damage !!!')
        return

    def announce_winner(self, evaluated_win):
        if evaluated_win is None:
            delayed_typing('Unbelievable! Its a draw!')
            sleep(2)
            return
        delayed_typing('Aaaand the winner iiiiiiis.....')
        if evaluated_win:
            delayed_typing(self.player_robot.name)
        else:
            delayed_typing(self.opponent_robot.name)
        sleep(1)
        return

    def exhausted_outcome(self):
        delayed_typing('Oh no! Both bots are out of energy and are unable to continue.')
        sleep(1)
        delayed_typing('We have to call it a draw... Next time, keep an eye on that battery folks!')
        
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
