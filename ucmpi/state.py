"""
System state management.
"""

from models import (
    ZoneEvent,
    ModeChangeEvent,
    AlarmModeEvent,
    PanelStatusEvent,
    ArmingEvent,
    DelayEvent
)


class SystemState:
    """Maintains the current state of the Comfort system."""

    def __init__(self):

        self.zones = {}

        self.mode = "off"

        self.alarm_mode = 0

        self.panel_status = 0

        self.alarm_status = "off"

    def update(self, event):

        #
        # Zone state
        #
        if isinstance(event, ZoneEvent):

            self.zones[event.zone] = event.state

        #
        # Panel mode changes
        #
        elif isinstance(event, ModeChangeEvent):

            self.mode = event.mode

            if event.mode in (
                "off",
                "away",
                "night",
                "day",
                "vacation"
            ):
                self.alarm_status = event.mode

        #
        # Alarm mode changes
        #
        elif isinstance(event, AlarmModeEvent):

            self.alarm_mode = event.mode

        #
        # Panel status
        #
        elif isinstance(event, PanelStatusEvent):

            self.panel_status = event.status

        #
        # Arming state
        #
        elif isinstance(event, ArmingEvent):

            if event.ready:
                self.alarm_status = "arming"
            else:
                self.alarm_status = "arming waiting on zone"

        #
        # Entry / Exit delay
        #
        elif isinstance(event, DelayEvent):

            if event.delay_type == "entry":
                self.alarm_status = "entry delay"
            else:
                self.alarm_status = "exit delay"

    def get_alarm_status(self):

        return self.alarm_status