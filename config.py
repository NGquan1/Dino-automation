from dataclasses import dataclass


@dataclass(frozen=True)
class Region:
    left: int
    top: int
    width: int
    height: int

    def as_mss_monitor(self) -> dict[str, int]:
        return {
            "left": self.left,
            "top": self.top,
            "width": self.width,
            "height": self.height,
        }


@dataclass(frozen=True)
class Settings:
    bottom_region: Region = Region(left=230, top=660, width=180, height=70)
    top_region: Region = Region(left=230, top=600, width=180, height=50)
    detection_threshold: int = 50
    action_cooldown_seconds: float = 0.3
    duck_duration_seconds: float = 0.4
    startup_delay_seconds: float = 3.0
    debug_mode: bool = False


DEFAULT_SETTINGS = Settings()
