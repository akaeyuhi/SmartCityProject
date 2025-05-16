from dataclasses import dataclass

@dataclass
class Temperature:
    value: float
    unit: str = "C"

    def __post_init__(self):
        if self.unit not in ('C', 'F'):
            raise ValueError(f"Unsupported temperature unit: {self.unit}")