import pytest

from controller import Action, Controller, ObstacleType, Observation


@pytest.fixture
def controller():
    return Controller(jump_distance=100, duck_distance=100)


def test_low_obstacle_causes_jump(controller):
    observation = Observation(ObstacleType.LOW, distance=80)

    assert controller.choose_action(observation) == Action.JUMP


def test_flying_obstacle_causes_duck(controller):
    observation = Observation(ObstacleType.FLYING, distance=80)

    assert controller.choose_action(observation) == Action.DUCK


def test_distant_obstacle_does_not_trigger_action(controller):
    observation = Observation(ObstacleType.LOW, distance=101)

    assert controller.choose_action(observation) == Action.NONE


def test_no_obstacle_does_not_trigger_action(controller):
    observation = Observation(ObstacleType.NONE)

    assert controller.choose_action(observation) == Action.NONE


def test_negative_action_distance_is_rejected():
    with pytest.raises(ValueError):
        Controller(jump_distance=-1)
