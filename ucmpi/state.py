"""
System state management.
"""

from models import (
    ZoneEvent,
    ModeChangeEvent,
    AlarmModeEvent,
    PanelStatusEvent
)


class SystemState:
    """Maintains the current state of the Comfort system."""

    def __init__(self):

        self.zones = {}

        self.mode = "off"

        self.alarm_mode = 0

        self.panel_status = 0

    def update(self, event):

        if isinstance(event, ZoneEvent):

            self.zones[event.zone] = event.state

        elif isinstance(event, ModeChangeEvent):

            self.mode = event.mode

        elif isinstance(event, AlarmModeEvent):

            self.alarm_mode = event.mode

        elif isinstance(event, PanelStatusEvent):

            self.panel_status = event.status

    def dump(self):

        print("\n----- SYSTEM STATE -----")

        print(f"Mode: {self.mode}")

        print(f"Alarm Mode: {self.alarm_mode}")

        print(f"Panel Status: {self.panel_status}")

        print("Active Zones:")

        active = [
            zone
            for zone, state
            in self.zones.items()
            if state
        ]

        if active:

            print(
                ", ".join(
                    str(zone)
                    for zone in sorted(active)
                )
            )

        else:

            print("None")

        print("------------------------\n")