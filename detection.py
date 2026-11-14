"""Illustrative sensor-threshold detector.

Caution: Wearing a sensor on a moving foot produces different signals from
wrist/chest-mounted datasets. This state machine has NOT been clinically validated.
"""
from dataclasses import dataclass
from enum import Enum, auto
from math import sqrt
from typing import Optional


@dataclass(frozen=True)
class MotionSample:
    timestamp_ms: int
    ax_g: float
    ay_g: float
    az_g: float
    gx_dps: float
    gy_dps: float
    gz_dps: float

    @property
    def acceleration_g(self) -> float:
        return sqrt(self.ax_g**2 + self.ay_g**2 + self.az_g**2)

    @property
    def rotation_dps(self) -> float:
        return sqrt(self.gx_dps**2 + self.gy_dps**2 + self.gz_dps**2)


@dataclass(frozen=True)
class DetectorConfig:
    freefall_g: float = 0.55
    impact_g: float = 2.3
    max_impact_delay_ms: int = 1000
    confirmation_window_ms: int = 4000
    still_accel_tolerance_g: float = 0.2
    still_rotation_dps: float = 25.0
    min_stillness_ms: int = 1000
    cooldown_ms: int = 5000

    def __post_init__(self) -> None:
        if not 0 < self.freefall_g < 1:
            raise ValueError("freefall_g must be between 0 and 1")
        if self.impact_g <= 1:
            raise ValueError("impact_g must exceed 1")
        if min(self.max_impact_delay_ms, self.confirmation_window_ms,
               self.min_stillness_ms, self.cooldown_ms) <= 0:
            raise ValueError("time windows must be positive")


@dataclass(frozen=True)
class FallAlert:
    timestamp_ms: int
    impact_timestamp_ms: int
    reason: str = "experimental fall-like motion (freefall -> impact -> stillness)"


class _Phase(Enum):
    IDLE = auto()
    AWAIT_IMPACT = auto()
    AWAIT_STILLNESS = auto()
    COOLDOWN = auto()


class FallDetector:
    """Requires a possible low-g interval, subsequent impact, then stillness.

    Experimental thresholds are examples, not proven human fall thresholds.
    This design can miss real falls and can trigger on non-falls.
    """

    def __init__(self, config: Optional[DetectorConfig] = None):
        self.config = config or DetectorConfig()
        self.reset()

    def reset(self) -> None:
        self.phase = _Phase.IDLE
        self._phase_start_ms = None
        self._impact_ms = None
        self._still_start_ms = None
        self._cooldown_until_ms = None
        self._last_timestamp = None

    def process(self, sample: MotionSample) -> Optional[FallAlert]:
        t = sample.timestamp_ms
        if self._last_timestamp is not None and t <= self._last_timestamp:
            raise ValueError("sample timestamps must be strictly increasing")
        self._last_timestamp = t

        if self.phase == _Phase.COOLDOWN:
            if t < self._cooldown_until_ms:
                return None
            self.phase = _Phase.IDLE

        a = sample.acceleration_g
        if self.phase == _Phase.IDLE:
            if a < self.config.freefall_g:
                self.phase = _Phase.AWAIT_IMPACT
                self._phase_start_ms = t
            return None

        if self.phase == _Phase.AWAIT_IMPACT:
            if t - self._phase_start_ms > self.config.max_impact_delay_ms:
                self.phase = _Phase.IDLE
                # Permit a new freefall to start on the current sample.
                if a < self.config.freefall_g:
                    self.phase = _Phase.AWAIT_IMPACT
                    self._phase_start_ms = t
            elif a >= self.config.impact_g:
                self.phase = _Phase.AWAIT_STILLNESS
                self._impact_ms = t
                self._still_start_ms = None
            return None

        if self.phase == _Phase.AWAIT_STILLNESS:
            if t - self._impact_ms > self.config.confirmation_window_ms:
                self.phase = _Phase.IDLE
                return None
            still = (abs(a - 1.0) <= self.config.still_accel_tolerance_g and
                     sample.rotation_dps <= self.config.still_rotation_dps)
            if still:
                if self._still_start_ms is None:
                    self._still_start_ms = t
                elif t - self._still_start_ms >= self.config.min_stillness_ms:
                    alert = FallAlert(timestamp_ms=t, impact_timestamp_ms=self._impact_ms)
                    self.phase = _Phase.COOLDOWN
                    self._cooldown_until_ms = t + self.config.cooldown_ms
                    return alert
            else:
                self._still_start_ms = None
        return None
