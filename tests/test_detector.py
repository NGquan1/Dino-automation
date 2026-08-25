import cv2
import numpy as np

from detector import detect_obstacle
from main import is_obstacle_detected


def test_detector_finds_dark_obstacle_on_light_background():
    frame = np.full((50, 180, 3), 255, dtype=np.uint8)
    cv2.rectangle(frame, (80, 10), (110, 40), (0, 0, 0), thickness=-1)

    assert is_obstacle_detected(frame)


def test_detector_ignores_uniform_background():
    frame = np.full((50, 180, 3), 255, dtype=np.uint8)

    assert not is_obstacle_detected(frame)


def test_detector_uses_configured_threshold():
    frame = np.full((20, 20, 3), 200, dtype=np.uint8)
    frame[5:15, 5:15] = 150

    assert not is_obstacle_detected(frame, threshold=60)
    assert is_obstacle_detected(frame, threshold=40)


def test_contour_detector_returns_obstacle_bounds():
    frame = np.full((50, 180, 3), 255, dtype=np.uint8)
    cv2.rectangle(frame, (80, 10), (110, 40), (0, 0, 0), thickness=-1)

    detection = detect_obstacle(frame)

    assert detection is not None
    assert detection.x == 80
    assert detection.y == 10
    assert detection.width == 31
    assert detection.height == 31
    assert detection.center_x == 95.5


def test_contour_detector_ignores_small_noise():
    frame = np.full((50, 180, 3), 255, dtype=np.uint8)
    frame[10, 10] = (0, 0, 0)

    assert detect_obstacle(frame, min_area=20) is None
