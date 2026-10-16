"""
UCMPI data models.
"""

from dataclasses import dataclass


@dataclass
class ZoneEvent:
    zone: int
    state: bool


@dataclass
class ArmingEvent:
    zone: int
    ready: bool


@dataclass
class DelayEvent:
    delay_type: str
    seconds: int


@dataclass
class ModeChangeEvent:
    mode: str
    user: int


@dataclass
class AlarmModeEvent:
    mode: int
    user: int


@dataclass
class PanelStatusEvent:
    status: int


@dataclass
class DateTimeEvent:
    timestamp: str


@dataclass
class AlarmEvent:
    code: str