from dataclasses import dataclass

import cv2
import numpy as np


@dataclass(frozen=True)
class ObstacleDetection:
    x: int
    y: int
    width: int
    height: int
    area: float

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2


def detect_obstacle(
    frame_roi: np.ndarray,
    threshold: int = 50,
    min_area: int = 20,
) -> ObstacleDetection | None:
    """Find the most significant dark connected component in an ROI."""
    if frame_roi.size == 0:
        return None
    if threshold < 0 or threshold > 255:
        raise ValueError("threshold must be between 0 and 255")
    if min_area < 1:
        raise ValueError("min_area must be positive")

    gray_roi = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2GRAY)
    background_level = float(np.median(gray_roi))
    dark_pixel_distance = background_level - gray_roi
    binary = np.where(dark_pixel_distance > threshold, 255, 0).astype(np.uint8)

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = [contour for contour in contours if cv2.contourArea(contour) >= min_area]
    if not candidates:
        return None

    contour = max(candidates, key=cv2.contourArea)
    x, y, width, height = cv2.boundingRect(contour)
    return ObstacleDetection(x, y, width, height, cv2.contourArea(contour))
