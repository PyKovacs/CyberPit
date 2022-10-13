import random
from abc import ABC, abstractmethod
from time import sleep
from typing import Optional

from src.robots import Robot
from src.users import User
from src.utils import clear_console, delayed_typing


class Opponent:
    def __init__(self, robot: Robot) -> None:
        self.robot = robot

    def accepted(self) -> bool:
        print('Ready for the fight?\n')
        sleep(.5)
        print(f'You stand against {self.robot.name}.')
        print(self.robot)
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


class Fight:
    def __init__(
            self,
            player: User,
            opponent: Opponent,
            round_runner: 'RoundRunner'
            ):

        self.player = player
        self.opponent = opponent
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

    def has_winner(self) -> bool:
        clear_console()
        round_count = 1
        while True:
            if self.player.robot.health <= 0 or self.opponent.robot.health <= 0:
                return True
            if self.player.robot.is_exhausted() and self.opponent.robot.is_exhausted():
                return False
            self.round_runner.start_round(round_count, self.player, self.opponent)
            round_count += 1


class RoundRunner:
    def start_turn(self, turn: 'Turns'):
        turn.execute()

    def start_round(self, round_count: int, player: User, opponent: Opponent):
        print(f'-------- ROUND {round_count} --------')
        self.start_turn(PlayersTurn(player, opponent))
        self.start_turn(OpponentsTurn(player, opponent))
        print('------------------------------------')


class Turns(ABC):
    def __init__(self, player: User, opponent: Opponent):
        self.player = player
        self.opponent = opponent

    @abstractmethod
    def execute(self):
        pass

    def status_check(self, robot: Robot) -> bool:
        if robot.is_exhausted():
            delayed_typing(f' -> {robot.name} is out of energy.')
            return False
        if robot.health <= 0:
            return False
        return True

    def attack(self, weapon: str, attacking: Robot, attacked: Robot) -> bool:
        weapon_energy = attacking.use_weapon(weapon)
        if weapon_energy == -1:
            delayed_typing('  -> not enough energy...')
            return False
        delayed_typing(f' -> {attacking.name} loading {weapon} ...')
        sleep(1)
        if not weapon_energy:
            delayed_typing(f'  -> {attacking.name} missed !!!')
            return True
        hit = attacked.take_damage(weapon_energy)
        if not hit:
            delayed_typing(f'  -> {attacked.name} dodged !!!')
            return True
        delayed_typing(f'  -> {attacked.name} took {weapon_energy} points of damage !!!')
        return True


class PlayersTurn(Turns):
    def execute(self) -> None:
        if not self.status_check(self.player.robot):
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
        if not self.status_check(self.opponent.robot):
            return
        weapons_available = [weapon for weapon in self.opponent.robot.weapons
                             if self.opponent.robot.energy
                             >= self.opponent.robot.get_weapon_energy(weapon)]
        weapon = random.choice(weapons_available)
        self.attack(weapon, self.opponent.robot, self.player.robot)


class OutcomeEval:
    def __init__(self, player_robot: Robot, opponent_robot: Robot):
        self.player_robot = player_robot
        self.opponent_robot = opponent_robot

    def announce_winner(self):
        delayed_typing('Aaaand the winner iiiiiiis.....')
        sleep(.5)
        if self.player_won():
            delayed_typing(f'\n  === {self.player_robot.name.upper()} ===')
        else:
            delayed_typing(f'\n  === {self.opponent_robot.name.upper()} ===')
        sleep(1)

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
        else:
            return True


def run(user: User, generated_robot: Robot):
    opponent = Opponent(generated_robot)
    outcome = OutcomeEval(user.robot, opponent.robot)
    if opponent.accepted():
        fight = Fight(user, opponent, RoundRunner())
        if fight.has_winner():
            outcome.announce_winner()
        else:
            outcome.exhausted_outcome()
        user.robot.reset()
        input('\nPress any key to continue to main menu...')
