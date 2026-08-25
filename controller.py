from dataclasses import dataclass
from enum import Enum


class ObstacleType(str, Enum):
    NONE = "none"
    LOW = "low"
    FLYING = "flying"


class Action(str, Enum):
    NONE = "none"
    JUMP = "jump"
    DUCK = "duck"


@dataclass(frozen=True)
class Observation:
    obstacle: ObstacleType
    distance: int = 0


class Controller:
    def __init__(self, jump_distance: int = 180, duck_distance: int = 180):
        if jump_distance < 0 or duck_distance < 0:
            raise ValueError("Action distances must be non-negative")
        self.jump_distance = jump_distance
        self.duck_distance = duck_distance

    def choose_action(self, observation: Observation) -> Action:
        if observation.obstacle == ObstacleType.FLYING and observation.distance <= self.duck_distance:
            return Action.DUCK
        if observation.obstacle == ObstacleType.LOW and observation.distance <= self.jump_distance:
            return Action.JUMP
        return Action.NONE
