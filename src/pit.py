import random
from abc import ABC, abstractmethod
from time import sleep

from src.robots import Robot, Weapons
from src.users import User
from src.utils import FightRecorder, clear_console, drama_print, safe_get


class Fight:
    """Main class where actual fight is happening."""
    def __init__(
            self,
            player: Robot,
            opponent: Robot,
            round_runner: 'RoundRunner',
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

    def has_winner(self, recorder: FightRecorder) -> bool:
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
                                          recorder,
                                          self.player,
                                          self.opponent)
            round_count += 1

    def _welcome_sequence(self) -> None:
        """Print welcome sequence before the fight."""
        clear_console()
        try:
            drama_print('LAAAAADIEEEES AND GENTLEMEEEEEN...')
            sleep(0.5)
            drama_print('Welcome, to THE CYBER PIT!\n')
            sleep(0.2)
            drama_print('A place where metal meets metal in '
                        'THE MOST SPECTACULAR ROOBOOOT FIIIGTHS!')
            sleep(0.5)
            drama_print(f'Tonight, {self.player.name} will confront '
                        f'{self.opponent.name} in unprecedented cyber dance.\n')
            sleep(1)
            drama_print('LET THE SHOOOOOOOW BEGIIIIIIIINNN !!!!', 0.08)
            sleep(2)
        except KeyboardInterrupt:
            pass
        clear_console()


class RoundRunner:
    """Helper class to call correct turn (player vs opponent)."""

    def start_turn(self, turn: 'Turn') -> None:
        """Execute turn based on Turn instance passed as argument."""
        turn.execute()

    def start_round(self, count: int, recorder: FightRecorder, player: Robot, opponent: Robot) -> None:
        """Execute Players and Opponents turn within one round."""
        recorder.record_event(f'-------- ROUND {count} --------', 0)
        self.start_turn(PlayersTurn(player, opponent, recorder))
        self.start_turn(OpponentsTurn(player, opponent, recorder))


class Turn(ABC):
    """Abstract class for turn."""

    def __init__(self, player: Robot, opponent: Robot, recorder: FightRecorder) -> None:
        self.player = player
        self.opponent = opponent
        self.recorder = recorder

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
            self.recorder.record_event(f' -> {robot.name} is out of energy.')
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
            drama_print('  -> not enough energy...')
            return False
        self.recorder.record_event(f' -> {attacking.name} loading {weapon} ...')
        sleep(1)
        if not weapon_energy:
            self.recorder.record_event(f'  -> {attacking.name} missed !!!')
            return True
        hit = attacked.take_damage(weapon_energy)
        if not hit:
            self.recorder.record_event(f'  -> {attacked.name} dodged !!!')
            return True
        self.recorder.record_event(f'  -> {attacked.name} took {weapon_energy} '
                       'points of damage !!!')
        return True


class PlayersTurn(Turn):
    def execute(self) -> None:
        """Display options for players turn and evaluates input."""
        if not self.status_check(self.player):
            return
        clear_console()
        print(self._get_banner(),
              self.recorder.get_records(),
              sep='\n')
        while True:
            action = input('Choose your weapon: ').lower()
            if action in self.player.weapons:
                if self.attack(action, self.player, self.opponent):
                    break

    def _get_banner(self) -> str:
        """Return a banner with names, energy and health bars, weapons."""
        pad: int = max(self.player.get_init_energy(),
                        self.player.get_init_health(),
                        self.opponent.get_init_energy(),
                        self.opponent.get_init_health()) +9
        return (f'|{self.player.name:^{pad}}'
                f'{self.opponent.name:^{pad}}|\n'
                f'|{" "*(2*pad)}|\n'
                f'|{self._get_health_bar(self.player):^{pad}}'
                f'{self._get_health_bar(self.opponent):^{pad}}|\n'
                f'|{self._get_energy_bar(self.player):^{pad}}'
                f'{self._get_energy_bar(self.opponent):^{pad}}|\n'
                f'{self._get_weapons(pad)}'
                f'|{"_" * pad * 2}|\n')

    def _get_health_bar(self, robot: Robot) -> str:
        """Return health bar for specific robot formatted for banner."""
        max_health = robot.get_init_health()
        current_health = robot.health
        return f'HP-[{"#" * current_health}{"-" * (max_health-current_health)}]'

    def _get_energy_bar(self, robot: Robot) -> str:
        """Return energy bar for specific robot formatted for banner."""
        max_energy = robot.get_init_energy()
        current_energy = robot.energy
        return f'EN-[{"#" * current_energy}{"-" * (max_energy-current_energy)}]'

    def _get_weapons(self, pad: int) -> str:
        """Return weapons list formatted for banner."""
        output = ''
        for idx in range(max(len(self.player.weapons), len(self.opponent.weapons))):
            weapon_p = safe_get(self.player.weapons, idx)
            content_p = f'{weapon_p}  -  {Weapons.get_energy(weapon_p)}'
            weapon_o = safe_get(self.opponent.weapons, idx)
            content_o = f'{weapon_o}  -  {Weapons.get_energy(weapon_o)}'
            output += (f'|{content_p:^{pad}}'
                       f'{content_o:^{pad}}|\n')
        return output


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
        print('--------------------------------')
        drama_print('Aaaand the winner iiiiiiis.....')
        sleep(.5)
        if self.player_won():
            drama_print(f'\n  === {self.player.name.upper()} ===\n')
            user.get_btc(int((self.opponent.cost / 10) * 2))
        else:
            drama_print(f'\n  === {self.opponent.name.upper()} ===')
        sleep(1)

    def exhausted_outcome(self) -> None:
        """Sequence when both bots are out of energy."""
        drama_print('Oh no! Both bots are out of energy '
                       'and are unable to continue.')
        sleep(1)
        drama_print('We have to call it a draw... '
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
    if (accepted := fight.accepted()) and fight.has_winner(FightRecorder()):
        outcome.announce_winner(user)
    elif accepted:
        outcome.exhausted_outcome()
    user.robot.reset()
    input('\nPress any key to continue to main menu...')
