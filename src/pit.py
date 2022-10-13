import random
import string
from abc import ABC, abstractmethod
from time import sleep
from typing import Optional

from src.robots import Robot, RobotManager
from src.users import User
from src.utils import clear_console, delayed_typing


class Opponent:
    def __init__(self, robot_manager: RobotManager) -> None:
        self.robot = self.generate_opponent(robot_manager)
        self.accepted = self.challenge()

    def generate_opponent(self, robot_manager: RobotManager) -> Robot:
        print('Ready for the fight?\n')
        sleep(.5)
        opp_build = random.choice(robot_manager.get_all_build_names())
        robot = Robot(opp_build, robot_manager.get_build_data(opp_build))
        robot.name = self.random_name()
        print(f'You stand against {robot.name}.')
        print(robot)
        return robot

    def challenge(self) -> bool:
        print('Last chance to give up.',
              'Type "flee" to go back to main menu.',
              'or "fight" to continue to the pit.',
              sep='\n')
        while True:
            f_or_f = input('Flight or fight? ').lower()
            if f_or_f in ['flee', 'flight']:
                return False
            if f_or_f == 'fight':
                return True

    def random_name(self) -> str:
        first = random.choice(string.ascii_letters)
        second = random.choice(string.ascii_letters)
        num = random.randint(100, 999)
        return f'{first}{second}-{num}'


class Fight:
    def __init__(
            self,
            player: User,
            opponent: Opponent,
            outcome: 'Outcome',
            round_runner: 'RoundRunner'
            ):

        self.player = player
        self.opponent = opponent
        self.outcome = outcome
        self.round_runner = round_runner
        self.welcome_sequence()

    def welcome_sequence(self) -> None:
        clear_console()
        delayed_typing('LAAAAADIEEEES AND GENTLEMEEEEEN...')
        sleep(0.5)
        delayed_typing('Welcome, to THE CYBER PIT!\n')
        sleep(0.2)
        delayed_typing('A place where metal meets metal in the MOST BRUUUUTAL ROOBOOOT FIIIGTHS!')
        sleep(0.5)
        delayed_typing(f'Tonight, {self.player.robot.name} will confront {self.opponent.robot.name} in unprecedented cyber dance.\n')
        sleep(1)
        delayed_typing(f'LET THE SHOOOOOOOW BEGIIIIIIIINNN !!!!', 0.08)
        sleep(2)
        clear_console()

    def start(self):
        clear_console()
        round_count = 1
        while True:
            if self.player.robot.health <= 0 or self.opponent.robot.health <= 0:
                # match finished
                self.outcome.announce_winner(self.outcome.player_won())
                break
            if self.player.robot.is_exhausted() and self.opponent.robot.is_exhausted():
                # match finished
                self.outcome.exhausted_outcome()
                break
            self.round_runner.start_round(round_count, self.player, self.opponent)
            round_count += 1


class RoundRunner:
    def start_turn(self, turn: 'Turns'):
        turn.execute()

    def start_round(self, round_count: int, player: User, opponent: Opponent):
        print(f'-------- ROUND {round_count} --------')
        self.start_turn(PlayersTurn(player, opponent))
        self.start_turn(OpponentsTurn(player, opponent))
        print(f'------------------------------------')


class Turns(ABC):
    def __init__(self, player: User, opponent: Opponent):
        self.player = player
        self.opponent = opponent

    @abstractmethod
    def execute(self):
        pass

    def energy_check(self, robot: Robot) -> bool:
        if robot.is_exhausted():
            delayed_typing(f' -> {robot.name} is out of energy.')
            return False
        return True

    def attack(self, weapon: str, attacking: Robot, attacked: Robot) -> bool:
        damage_points = attacking.use_weapon(weapon)
        if damage_points == -1:
            delayed_typing('  -> not enough energy...')
            return False
        delayed_typing(f' -> {attacking.name} loading {weapon} ...')
        sleep(1)
        if not damage_points:
            delayed_typing(f'  -> {attacking.name} missed !!!')
            return True
        hit = attacked.take_damage(damage_points)
        if not hit:
            delayed_typing(f'  -> {attacked.name} dodged !!!')
            return True
        delayed_typing(f'  -> {attacked.name} took {damage_points} points of damage !!!')
        return True


class PlayersTurn(Turns):
    def execute(self) -> None:
        if not self.energy_check(self.player.robot):
            return
        print(f'\nYour weapons: {self.player.robot.weapons}')
        print('You have following options:\n',
              ' - type the weapon name to use it',
              ' - type "stats" for your robot current stats',
              ' - type "enemy" for your enemy\'s stats',
              sep='\n')
        while True:
            action = input('What will it be? ').lower()
            if action == 'stats':
                print(self.player.robot)
            if action == 'enemy':
                print(self.opponent.robot)
            if action in self.player.robot.weapons:
                if self.attack(action, self.player.robot, self.opponent.robot):
                    break


class OpponentsTurn(Turns):
    def execute(self):
        if not self.energy_check(self.opponent.robot):
            return
        weapons_available = [weapon for weapon in self.opponent.robot.weapons
                             if self.opponent.robot.energy
                             >= self.opponent.robot.get_weapon_energy(weapon)]
        weapon = random.choice(weapons_available)
        self.attack(weapon, self.opponent.robot, self.player.robot)


class Outcome:
    def __init__(self, player_robot: Robot, opponent_robot: Robot):
        self.player_robot = player_robot
        self.opponent_robot = opponent_robot

    def announce_winner(self, player_won):
        if player_won is None:
            delayed_typing('Unbelievable! Its a draw!')
            sleep(2)
            return
        delayed_typing('Aaaand the winner iiiiiiis.....')
        if player_won:
            delayed_typing(self.player_robot.name)
        else:
            delayed_typing(self.opponent_robot.name)
        sleep(1)
        return

    def exhausted_outcome(self):
        delayed_typing('Oh no! Both bots are out of energy and are unable to continue.')
        sleep(1)
        delayed_typing('We have to call it a draw... Next time, keep an eye on that battery folks!')

    def player_won(self) -> Optional[bool]:
        '''
        Returns the winner of the match
        '''
        if self.opponent_robot.health > self.player_robot.health:
            return False
        elif self.opponent_robot.health < self.player_robot.health:
            return True
        else:
            return None


def run(user: User, robot_manager: RobotManager):
    opponent = Opponent(robot_manager)
    if opponent.accepted:
        fight = Fight(user, opponent, Outcome(user.robot, opponent.robot), RoundRunner())
        fight.start()
        user.robot.reset(robot_manager)
        input('\nPress any key to continue to main menu...')
