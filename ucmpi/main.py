from comfort import ComfortConnection
from protocol import ComfortProtocol
from mqtt import MQTTPublisher

from models import ZoneEvent

from state import SystemState

from pathlib import Path

from configuration import (
    ComfortConfiguration
)

from homeassistant import (
    HomeAssistantDiscovery
)


def main():

    comfort = ComfortConnection()

    protocol = ComfortProtocol()

    mqtt = MQTTPublisher()

    state = SystemState()

    config = ComfortConfiguration()

    config_file = (
        Path(__file__).resolve().parent
        / "comfort_export.txt"
    )

    config.load_xml(str(config_file))

    ha = HomeAssistantDiscovery(
        mqtt
    )

    ha.publish_alarm_discovery()

    comfort.connect()

    print("Waiting for Comfort messages...\n")

    while True:

        message = comfort.read_message()

        if not message:
            continue

        event = protocol.parse(message)

        if not event:
            print(
                f"Unhandled message: "
                f"{message}"
            )
            continue

        #
        # Update system state
        #
        state.update(event)

        #
        # Display events
        #
        if isinstance(event, ZoneEvent):

            zone_name = config.get_zone_name(
                event.zone
            )

            print(
                f"{zone_name} -> "
                f"{'ON' if event.state else 'OFF'}"
            )

            mqtt.publish_zone(
                event.zone,
                event.state
            )

        else:

            print(event)

        #
        # Publish Home Assistant alarm state
        #
        alarm_status = (
            state.get_alarm_status()
        )

        print(
            f"Alarm Status: "
            f"{alarm_status}"
        )

        ha.publish_alarm_state(
            alarm_status
        )


if __name__ == "__main__":
    main()