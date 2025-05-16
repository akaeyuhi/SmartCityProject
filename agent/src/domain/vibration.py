from dataclasses import dataclass, field
import math


@dataclass
class Vibration:
    x: float
    y: float
    z: float
    magnitude: float = field(init=False)

    def __post_init__(self):
        self.magnitude = math.sqrt(self.x**2 + self.y**2 + self.z**2)