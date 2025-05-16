from dataclasses import dataclass


@dataclass
class Light:
    illumination: float  # in lux

    def is_dark(self, threshold: float = 10.0) -> bool:
        return self.illumination < threshold