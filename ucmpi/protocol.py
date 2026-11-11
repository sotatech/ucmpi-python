"""
Comfort protocol parser.
"""

from models import (
    ZoneEvent,
    ArmingEvent,
    DelayEvent,
    ModeChangeEvent,
    AlarmModeEvent,
    PanelStatusEvent,
    DateTimeEvent,
    LoginEvent,
    AlarmEvent
)


class ComfortProtocol:
    """Parses Comfort protocol messages."""

    MODES = {
        0: "off",
        1: "away",
        2: "night",
        3: "day",
        4: "vacation"
    }

    def parse(self, message: str):

        #
        # Login response
        #
        if message.startswith("LU"):

            user = int(message[2:])

            return LoginEvent(
                user=user
            )

        #
        # Input Point (Zone)
        #
        elif message.startswith("IP"):

            zone = int(message[2:4], 16)

            state = (
                message[4:6] == "01"
            )

            return ZoneEvent(
                zone=zone,
                state=state
            )

        #
        # Arming Status
        #
        elif message.startswith("ER"):

            zone = int(
                message[2:4],
                16
            )

            return ArmingEvent(
                zone=zone,
                ready=(zone == 0)
            )

        #
        # Entry / Exit Delay
        #
        elif message.startswith("EX"):

            delay_type = (
                "entry"
                if message[2:4] == "01"
                else "exit"
            )

            seconds = int(
                message[4:],
                16
            )

            return DelayEvent(
                delay_type=delay_type,
                seconds=seconds
            )

        #
        # Mode Change
        #
        elif message.startswith("MD"):

            mode_number = int(
                message[2:4],
                16
            )

            user = int(
                message[4:6],
                16
            )

            mode = self.MODES.get(
                mode_number,
                f"unknown({mode_number})"
            )

            return ModeChangeEvent(
                mode=mode,
                user=user
            )

        #
        # Alarm Mode
        #
        elif message.startswith("AM"):

            mode = int(
                message[2:4],
                16
            )

        