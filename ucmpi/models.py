"""
UCMPI data models.
"""

from dataclasses import dataclass


@dataclass
class ZoneEvent:
    zone: int
    state: bool