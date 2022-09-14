
from dataclasses import dataclass

#Robots related dataclasses
@dataclass
class RobotBase:
    health: int = 20
    energy: int = 20
    dodge: int = 10
    miss_chance: int = 5
    cost: int = 500

@dataclass
class Heavy(RobotBase):
    health: int = 30
    dodge: int = 5
    desc: str = 'Heavy tank, increased HP.'
    cost: int = 300

@dataclass
class Light(RobotBase):
    health: int = 15
    dodge: int = 20
    desc: str = 'Light construction, good at dodging.'
    cost: int = 250


#############################
# User related dataclass
@dataclass
class User:
    name: str
    balance: int = 0
    robot: Any = None

    def set_balance(self, balance):
        self.balance = balance
    
    def set_robot(self, robot: Any):
        self.robot = robot