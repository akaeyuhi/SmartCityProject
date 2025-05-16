from dataclasses import dataclass


@dataclass
class Humidity:
    value: float
    unit: str = "%"

    def __post_init__(self):
        if not (0 <= self.value <= 100):
            raise ValueError("Humidity value must be between 0 and 100")