import random
from abc import ABC, abstractmethod
from time import sleep

from src.robots import Robot, Weapons
from src.users import User
from src.utils import clear_console, delayed_typing


class Fight:
    """Main class where actual fight is happening."""
    def __init__(
            self,
            player: Robot,
            opponent: Robot,
            round_runner: 'RoundRunner'
            ):

        self.player = player
        self.opponent = opponent
        self.round_runner = round_runner

    def accepted(self) -> bool:
        """
        Return True if challenge is accepted.

        Presents the opponent and ask the user if
        he/she wants to fight or flight.
        """
        print('Ready for the fight?\n')
        sleep(.5)
        print(f'You stand against {self.opponent.name}.')
        print(self.opponent)
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

    def has_winner(self) -> bool:
        """
        Loop round_runner until the end of fight.

        Return True if there is a winner.
        """
        self._welcome_sequence()
        round_count = 1
        while True:
            if self.player.health <= 0 or self.opponent.health <= 0:
                return True
            if self.player.is_exhausted() and self.opponent.is_exhausted():
                return False
            self.round_runner.start_round(round_count,
                                          self.player,
                                          self.opponent)
            round_count += 1

    def _welcome_sequence(self) -> None:
        """Print welcome sequence before the fight."""
        clear_console()
        try:
            delayed_typing('LAAAAADIEEEES AND GENTLEMEEEEEN...')
            sleep(0.5)
            delayed_typing('Welcome, to THE CYBER PIT!\n')
            sleep(0.2)
            delayed_typing('A place where metal meets metal in '
                        'THE MOST SPECTACULAR ROOBOOOT FIIIGTHS!')
            sleep(0.5)
            delayed_typing(f'Tonight, {self.player.name} will confront '
                        f'{self.opponent.name} in unprecedented cyber dance.\n')
            sleep(1)
            delayed_typing('LET THE SHOOOOOOOW BEGIIIIIIIINNN !!!!', 0.08)
            sleep(2)
        except KeyboardInterrupt:
            pass
        clear_console()

class RoundRunner:
    """Helper class to call correct turn (player vs opponent)."""

    def start_turn(self, turn: 'Turn') -> None:
        """Execute turn based on Turn instance passed as argument."""
        turn.execute()

    def start_round(self, count: int, player: Robot, opponent: Robot) -> None:
        """Execute Players and Opponents turn within one round."""
        print(f'-------- ROUND {count} --------')
        self.start_turn(PlayersTurn(player, opponent))
        self.start_turn(OpponentsTurn(player, opponent))
        print('------------------------------------')


class Turn(ABC):
    """Abstract class for turn."""

    def __init__(self, player: Robot, opponent: Robot) -> None:
        self.player = player
        self.opponent = opponent

    @abstractmethod
    def execute(self) -> None:
        """Abstract method for turn execution."""

    def status_check(self, robot: Robot) -> bool:
        """
        Evaluate if robot can make a turn.

        Return False if robot energy is below
        or equal to lowest weapon energy (exhausted).
        Also return False if health is below or equal to 0.
        """
        if robot.is_exhausted():
            delayed_typing(f' -> {robot.name} is out of energy.')
            return False
        if robot.health <= 0:
            return False
        return True

    def attack(self, weapon: str, attacking: Robot, attacked: Robot) -> bool:
        """
        Attack execution and evaluation.

        Return True if attack was performed.
        Return False if there is not enough energy to use the weapon.
        """
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
        delayed_typing(f'  -> {attacked.name} took {weapon_energy} '
                       'points of damage !!!')
        return True


class PlayersTurn(Turn):
    def execute(self) -> None:
        """Display options for players turn and evaluates input."""
        if not self.status_check(self.player):
            return
        self._display_options()
        while True:
            action = input('What will it be? ').lower()
            if action == 'stats':
                print(self.player)
                print(self.opponent)
            if action in self.player.weapons:
                if self.attack(action, self.player, self.opponent):
                    break

    def _display_options(self) -> None:     # TODO - health, energy bars, weapons list
        """Print playable options."""
        print(self._get_bars(self.player),
              self._get_bars(self.opponent),
              f'Your weapons: {self.player.weapons}',
              sep='\n')
        # print('You have following options:\n',
        #     ' - type the weapon name to use it',
        #     ' - type "stats" for robots current stats',
        #     sep='\n')
        
    # def _status_bars(self):
    #     enemy_bars = self._get_bars(self.opponent)
    #     player_bars = self._get_bars(self.player)
        

    def _get_bars(self, robot: Robot) -> str:
        max_health = robot._init_data['health']
        current_health = robot.health
        max_energy = robot._init_data['energy']
        current_energy = robot.energy
        assert isinstance(max_health, int) and isinstance(max_energy, int)
        health_bar = f'[{"#" * current_health}{"-" * (max_health-current_health)}]'
        energy_bar = f'[{"#" * current_energy}{"-" * (max_energy-current_energy)}]'
        return f'{robot.name} HP-{health_bar:<35} \t EN-{energy_bar}'
        
class OpponentsTurn(Turn):
    def execute(self) -> None:
        """Pick a random weapon from arsenal and execute attack."""
        if not self.status_check(self.opponent):
            return
        weapons_available = [weapon for weapon in self.opponent.weapons
                             if self.opponent.energy
                             >= Weapons.get_energy(weapon)]
        weapon = random.choice(weapons_available)
        self.attack(weapon, self.opponent, self.player)


class OutcomeEval:
    """Class for outcome evaluation and announcement."""
    def __init__(self, player: Robot, opponent: Robot) -> None:
        self.player = player
        self.opponent = opponent

    def announce_winner(self, user: User) -> None:
        """Evaluate, announce the winner and pays the player if won. """
        delayed_typing('Aaaand the winner iiiiiiis.....')
        sleep(.5)
        if self.player_won():
            delayed_typing(f'\n  === {self.player.name.upper()} ===\n')
            user.get_btc(int((self.opponent.cost / 10) * 2))
        else:
            delayed_typing(f'\n  === {self.opponent.name.upper()} ===')
        sleep(1)

    def exhausted_outcome(self) -> None:
        """Sequence when both bots are out of energy."""
        delayed_typing('Oh no! Both bots are out of energy '
                       'and are unable to continue.')
        sleep(1)
        delayed_typing('We have to call it a draw... '
                       'Next time, keep an eye on that battery folks!')

    def player_won(self) -> bool:
        """Return True if player won."""
        if self.opponent.health > self.player.health:
            return False
        return True


def run(user: User, opponent_robot: Robot) -> None:
    """Main function to run the pit."""
    fight = Fight(user.robot, opponent_robot, RoundRunner())
    outcome = OutcomeEval(user.robot, opponent_robot)
    if (accepted := fight.accepted()) and fight.has_winner():
        outcome.announce_winner(user)
    elif accepted:
        outcome.exhausted_outcome()
    user.robot.reset()
    input('\nPress any key to continue to main menu...')
