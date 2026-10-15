"""
Comfort protocol parser.
"""

from models import ZoneEvent


class ComfortProtocol:
    """Parses Comfort protocol messages."""

    def parse(self, message: str):

        if message.startswith("IP"):

            zone = int(message[2:4], 16)
            state = message[4:6] == "01"

            return ZoneEvent(
                zone=zone,
                state=state
            )

        return None