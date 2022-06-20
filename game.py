from dataclasses import dataclass
from typing import List

@dataclass
class Robot:
    name : str
    hp : int
    energy : int
    weapons : List[object]
    